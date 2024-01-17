import os
from supabase import create_client

class DatabaseConnector:
    _instance = None

    def __new__(cls, url=None, key=None):
        if not cls._instance:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            cls._instance.url = url or os.environ.get("SUPABASE_URL")
            cls._instance.key = key or os.environ.get("SUPABASE_KEY")
            cls._instance.connection = cls._instance.connect()
        return cls._instance

    def connect(self):
        try:
            connection = create_client(self.url, self.key)
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        if not self.connection:
            print("Not connected to the database.")
            return None

        try:
            result = self.connection.sql(query).execute()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
