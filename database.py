import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.connection = None
        self.database = 'python_car'
        self.host = 'localhost'
        self.user = 'root'
        self.password = os.getenv('DB_PASSWORD')

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.is_connected():
            self.connection.close()

    def is_connected(self):
        return self.connection is not None

    def insert(self, db_data):
        if self.is_connected():
            query = (
                "INSERT INTO training_table "
                "(generation, points, timeAlive, lapTime, hitWall, avgSpeed, weights) "
                "VALUES "
                "(%s, %s, %s, %s, %s, %s, %s)"
            )
            cursor = self.connection.cursor()
            for value in db_data:
                cursor.execute(query, [value[key] for key in value.keys()])
            cursor.close()

    def read(self):
        if self.is_connected():
            cursor = self.connection.cursor()
            cursor.execute('SELECT * from `products`')
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            return None

    def read_best(self):
        if self.is_connected():
            cursor = self.connection.cursor()
            cursor.execute('SELECT `weights` from training_table ORDER BY `points` desc')
            result = cursor.fetchall()
            cursor.close()
            return result[0], result[1]
        else:
            return None




