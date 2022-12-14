# Importando pacotes e módulos
import psycopg2
import json
import datetime
import pytz

# Lendo o arquivo de parâmetros
with open("./dao/config.json", "rb") as file:
    config = json.load(file)

# Database access class
class DBAccess:

    # Connection parameters
    def __init__(self):
        self.host = config["host"]
        self.database = config["database"]
        self.user = config["user"]
        self.password = config["password"]
        self.port = config["port"]

    # Connnecting to the database
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            port=self.port,
            password=self.password
        )
        cursor = self.conn.cursor()
        return cursor

    # Disconnecting from the database
    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    # Reading every match
    def get_matches(self):
        cursor = self.connect()
        cursor.execute(f"""
                        SELECT id, datetime, team_1, goals_1, team_2, goals_2 FROM matches
                        ORDER BY id
                        """)                
        results = cursor.fetchall()
        self.disconnect()
        matches = []
        for result in results:
            match = {
                "id": result[0],
                "datetime": result[1].strftime("%d/%m/%Y %H:%M"),
                "team_1": result[2],
                "goals_1": result[3],
                "team_2": result[4],
                "goals_2": result[5]
            }
            matches.append(match)
        return matches

    # Reading guesses from a player
    def get_guesses(self, username):
        cursor = self.connect()
        cursor.execute("""
                       SELECT guesses, score FROM users
                       WHERE username = %s
                       """, (username,))                
        results = cursor.fetchone()
        score = results[1]
        result = results[0]
        if result is not None:
            guesses = {int(k): v for k, v in result.items()}
        else:
            guesses = result
        self.disconnect()
        return guesses, score

   # Reading data from every player for building the user list
    def get_users_management(self):
        cursor = self.connect()
        cursor.execute("""
                    SELECT name, username, score, password, admin_access FROM users
                    ORDER BY score DESC
                        """)              
        results = cursor.fetchall()
        self.disconnect()
        users = []
        for result in results:
            user = {
                "name": result[0],
                "username": result[1],
                "score": result[2],
                "password": result[3],
                "admin_access": result[4]
            }  
            if user["admin_access"] == False:
                users.append(user)
        return users

    # Reading data from every player for building the ranking
    def get_users_ranking(self):
        cursor = self.connect() 
        cursor.execute("""
                    SELECT name, username, score, exact_guesses FROM users
                    ORDER BY score DESC, exact_guesses DESC, name ASC
                        """)                
        results = cursor.fetchall()
        self.disconnect()
        users = []
        counter = 1
        last_score = -1
        cumulated_position = 1
        for result in results:
            if result[2] == last_score:
                position = cumulated_position
                position = counter
            else:
                position = counter
                cumulated_position = counter
                last_score = result[2]
            user = {
                "name": result[0],
                "username": result[1],
                "score": result[2],
                "position": position
            }
            users.append(user)
            counter += 1
        return users

    # Reding data from a player
    def get_user(self, username):
        cursor = self.connect()
        cursor.execute("""
                       SELECT name, username, password, admin_access FROM users
                       WHERE username = %s
                       """, (username,))                
        result = cursor.fetchone()
        self.disconnect()
        if result is None:
            user = None
        else:
            user = {
                "name": result[0],
                "username": result[1],
                "password": result[2],
                "admin_access": result[3]
            }
        return user

    # Adding a player
    def add_user(self, name, username, password):
        cursor = self.connect()
        cursor.execute("""
                       INSERT INTO users (username, password, name, admin_access, payment_status, score)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       """, (username, password, name, False, True, 0))                
        self.disconnect()

    # Deleting a player
    def delete_user(self, username):
        cursor = self.connect()
        cursor.execute("""
                       DELETE FROM users
                       WHERE username = %s
                       """, (username,))                
        self.disconnect()
    
    # Saving a new guess of a player
    def save_guess(self, username, match_id, goals_1, goals_2):
        cursor = self.connect()
        cursor.execute("""
                       SELECT guesses FROM users
                       WHERE username = %s
                       """, (username,)) 
        result = cursor.fetchone()
        guesses = result[0]
        if guesses is not None:
            updated_guesses = guesses
            updated_guesses[str(match_id)] = [goals_1, goals_2, 0]
        else:
            guesses = {}
            for i in range(48):
                guesses[str(i + 1)] = [None, None, 0]
            updated_guesses = guesses
            updated_guesses[str(match_id)] = [goals_1, goals_2, 0]
        cursor.execute("""
                       SELECT datetime FROM matches
                       WHERE id = %s
                       """, (match_id,))                
        result = cursor.fetchone()
        match_datetime = result[0]
        deadline = match_datetime - datetime.timedelta(hours=1)
        current_datetime = datetime.datetime.now(pytz.timezone("America/Sao_Paulo"))
        current_datetime = current_datetime.replace(tzinfo=None)
        if current_datetime >= deadline:
            raise Exception
        else:
            cursor.execute("""
                           UPDATE users SET guesses = %s
                           WHERE username = %s
                           """, (json.dumps(updated_guesses), username))                
        self.disconnect()

    # Updating a player
    def update_user(self, name, username, password):
        cursor = self.connect()
        cursor.execute("""
                       UPDATE users SET password = %s, name = %s
                       WHERE username = %s
                       """, (password, name, username))                
        self.disconnect()

    # Updating a match result
    def update_match(self, match_id, goals_1, goals_2):
        cursor = self.connect()
        cursor.execute("""
                       UPDATE matches SET goals_1 = %s, goals_2 = %s
                       WHERE id = %s
                       """, (goals_1, goals_2, match_id))                
        self.disconnect()

    # Updating score of a specific match for every user
    def update_scores(self, match_id, goals_1, goals_2):
        cursor = self.connect()
        cursor.execute("""
                       SELECT id, guesses FROM users
                       """)
        results = cursor.fetchall()
        for result in results:
            user_id = result[0]
            guesses = result[1]
            if guesses is not None:
                guesses = {int(k): v for k, v in guesses.items()}
                if goals_1 is not None and goals_2 is not None:
                    if None in guesses[match_id]:
                        guesses[match_id][2] = 0
                    else:
                        if guesses[match_id][0] == goals_1 and guesses[match_id][1] == goals_2:
                            guesses[match_id][2] = 5
                        elif guesses[match_id][0] > guesses[match_id][1] and goals_1 > goals_2:
                            guesses[match_id][2] = 3
                        elif guesses[match_id][0] < guesses[match_id][1] and goals_1 < goals_2:
                            guesses[match_id][2] = 3
                        elif guesses[match_id][0] == guesses[match_id][1] and goals_1 == goals_2:
                            guesses[match_id][2] = 3
                        else:
                            guesses[match_id][2] = 0
                else:
                    guesses[match_id][2] = 0
                cursor.execute("""
                            UPDATE users SET guesses = %s
                            WHERE id = %s
                            """, (json.dumps(guesses), user_id))                          
        self.disconnect()

    # Updating the total score of every user
    def sum_scores(self):
        cursor = self.connect()
        cursor.execute("""
                       SELECT id, guesses FROM users
                       """)
        results = cursor.fetchall()  
        for result in results:
            user_id = result[0]
            guesses = result[1]
            if guesses is None:
                total_score = 0
                exact_guesses = 0
            else:
                guesses = {int(k): v for k, v in guesses.items()}
                total_score = 0
                exact_guesses = 0
                for match_id in guesses.keys():
                    total_score += guesses[match_id][2]
                    if guesses[match_id][2] == 5:
                        exact_guesses += 1
            cursor.execute("""
                           UPDATE users SET score = %s, exact_guesses = %s
                           WHERE id = %s
                           """, (total_score, exact_guesses, user_id))          
        self.disconnect()

   # Reading guesses from all users for the same match
    def get_comparison(self, match_id):
        cursor = self.connect()
        cursor.execute("""
                       SELECT name, guesses FROM users
                       ORDER BY name
                        """)              
        results = cursor.fetchall()
        self.disconnect()
        users = []
        for result in results:
            if result[1] is None:
                user = {
                    "name": result[0],
                    "guess": ["Nulo", "Nulo", 0]
                }
            else:
                if None in result[1][str(match_id)]:
                    user = {
                        "name": result[0],
                        "guess": ["Nulo", "Nulo", 0]                        
                    }
                else:
                    user = {
                        "name": result[0],
                        "guess": result[1][str(match_id)]
                    }
            users.append(user)
        return users