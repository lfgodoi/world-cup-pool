# Importando pacotes e módulos
import psycopg2
import json
import datetime

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
        cursor.execute(f"""
                        SELECT guesses FROM users
                        WHERE cpf = '42431892859'
                        """)                
        result = cursor.fetchone()[0]
        guesses = {
            i + 1: [2, 5] 
            for i in range(48)
        }
        return guesses

    # Lendo os dados dos jogadores
    def get_users(self):
        cursor = self.connect()
        cursor.execute(f"""
                        SELECT name, cpf, score FROM users
                        ORDER BY score DESC
                        """)                
        results = cursor.fetchall()
        users = []
        counter = 1
        for result in results:
            user = {
                "name": result[0],
                "cpf": result[1][:-6] + '******',
                "score": result[2],
                "position": counter
            }
            users.append(user)
            counter += 1
        return users