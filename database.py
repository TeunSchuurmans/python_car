import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.connection = None
        self.database = 'webshop'
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
        if self.connection:
            self.connection.close()

    def is_connected(self):
        return self.connection is not None

    def insert(self, db_data):
        if self.is_connected():

            """
            what insert data should look like:
            
            id: auto ic
            points: self.npc.points
            weights: self.npc.nnet.weights
            generation: auto ic
            """

            cursor = self.connection.cursor()
            cursor.execute('INSERT INTO ')
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
            cursor.execute('SELECT `productID`, `productPrice` from `products` ORDER BY `productPrice`')
            result = cursor.fetchall()
            cursor.close()
            return result[0], result[1]
        else:
            return None




