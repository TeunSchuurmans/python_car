import mysql.connector


class Database:
    def __init__(self):
        self.connection = None
        self.database = 'webshop'
        self.host = 'localhost'
        self.user = 'root'
        self.password = '6Nj3LKfMYzvzyKr8'

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

    def insert(self):
        if self.is_connected():
            pass

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
            cursor.execute('SELECT * from `products`')
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            return None


database = Database()
database.connect()
print(database.read_best())


