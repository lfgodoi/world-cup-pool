# Importando pacotes e módulos
import psycopg2
import json

# Lendo o arquivo de parâmetros
with open("./dao/config.json", "rb") as file:
    config = json.load(file)

# Classe de acesso ao banco
class DBAccess:

    # Parâmetros de conexão
    def __init__(self):
        self.host = config["host"]
        self.database = config["database"]
        self.user = config["user"]
        self.password = config["password"]
        self.port = config["port"]

    # Conectando-se ao banco
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

    # Desconectando-se do banco
    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    # Lendo as partidas
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

    # Lendo os palpites de um jogador
    def get_guesses(self):
        cursor = self.connect()
        cursor.execute("""
                       SELECT guesses FROM users
                       WHERE username = 'lfgodoi'
                       """)                
        result = cursor.fetchone()[0]
        self.disconnect()
        guesses = {
            i + 1: [2, 5] 
            for i in range(48)
        }
        return guesses

    # Lendo os dados dos jogadores para gerenciamento
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

    # Lendo os dados dos jogadores para ranking
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

    # Lendo os dados de um jogador
    def get_user(self, username):
        cursor = self.connect()
        cursor.execute(f"""
                        SELECT name, username, password, admin_access FROM users
                        WHERE username = username
                        """)                
        result = cursor.fetchone()
        self.disconnect()
        user = {
            "name": result[0],
            "username": result[1],
            "password": result[2],
            "admin_access": result[3]
        }
        return user

    # Adicionando um jogador
    def add_user(self, name, username, password):
        cursor = self.connect()
        cursor.execute("""
                       INSERT INTO users (username, password, name, admin_access, payment_status, score)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       """, (username, password, name, False, True, 0))                
        self.disconnect()

    # Removendo um jogador
    def delete_user(self, username):
        cursor = self.connect()
        cursor.execute("""
                       DELETE FROM users
                       WHERE username = %s
                       """, (username,))                
        self.disconnect()
    
