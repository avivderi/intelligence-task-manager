import mysql.connector

class DB_connection:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password = '1234'
            )
        
    def get_conncation(self):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        return self.conn
    
    def create_database(self):
        with self.conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
            cursor.execute("USE Intelligence_db")
            self.conn.commit()


    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS agents(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            specialty VARCHAR(50) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            completed_missions INT DEFAULT 0,
            failed_missions INT DEFAULT 0,
            agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
            )
            '''
            )
        self.conn.commit()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS missions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(100) NOT NULL,
            difficulty INT NOT NULL,
            importance INT NOT NULL,
            status VARCHAR(30) DEFAULT 'NEW',
            risk_level VARCHAR(30) NOT NULL,
            assigned_agent_id INT DEFAULT NULL
            )
            '''
        )
        self.conn.commit()
        
        
    def close_db(self):
        self.conn.close()

DB = DB_connection()