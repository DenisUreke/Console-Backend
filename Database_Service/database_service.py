import sqlite3

class DatabaseService:
    def __init__(self, db_name="Database_Service/database.db"):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
    def execute(self, query,  params = None):
        if params is None:
            params = ()
        self.cur.execute(query, params)
        self.con.commit()
        
    def fetch_all(self, query, params = None):
        if params is None:
            params = ()
        self.cur.execute(query, params)
        return self.cur.fetchall()
    
    def fetch_one(self, query, params=None):
        if params is None:
            params = ()
        self.cur.execute(query, params)
        return self.cur.fetchone()
    
    def close(self):
        self.cur.close()
        self.con.close()
    
    # initial creation of database
    def initialize_schema(self, sql_path="Database_Service/tables.sql"):
        with open(sql_path, "r") as f:
            self.cur.executescript(f.read())
        self.con.commit()
        