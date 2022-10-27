# Importando pacotes e módulos
import psycopg2
import json

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
                "goals_2": result[3],
            }
            matches.append(match)
        return matches

    # Reading guesses from a player
    def get_guesses(self, username):
        cursor = self.connect()
        cursor.execute("""
                       SELECT guesses FROM users
                       WHERE username = %s
                       """, (username,))                
        result = cursor.fetchone()[0]
        if result is not None:
            guesses = {int(k): v for k, v in result.items()}
        else:
            guesses = result
        self.disconnect()
        return guesses

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
                    SELECT name, username, score FROM users
                    ORDER BY score DESC
                        """)                
        results = cursor.fetchall()
        self.disconnect()
        users = []
        counter = 1
        for result in results:
            user = {
                "name": result[0],
                "username": result[1],
                "score": result[2],
                "position": counter
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
    
    # Saving guesses of a player
    def save_guesses(self, username, guesses):
        cursor = self.connect()
        cursor.execute("""
                       UPDATE users SET guesses = %s
                       WHERE username = %s
                       """, (json.dumps(guesses), username))                
        self.disconnect()

    # Updating a player
    def update_user(self, name, username, password):
        cursor = self.connect()
        cursor.execute("""
                       UPDATE users SET password = %s, name = %s
                       WHERE username = %s
                       """, (password, name, username))                
        self.disconnect()