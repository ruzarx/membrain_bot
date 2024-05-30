import psycopg2
# import sqlalchemy
import pandas as pd

from data_structures import ReminderRecord

class DBConnect():

    def __get_db_connector(self):
        conn = psycopg2.connect(dbname='my_db', user='postgres', password='postgres', host='postgres', port=5432)
        conn.autocommit = True
        return conn
    
    def insert_data(self, table: str, record: ReminderRecord):
        # engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:postgres@postgres:5432/my_db")
        with self.__get_db_connector().cursor() as cursor:
            cursor.execute((f"""
                            INSERT INTO {table} (user_id, reminder_txt, reminder_date) VALUES 
                            ('{record.user_id}', '{record.reminder_txt}', '{record.reminder_date}')
                            """))
        print("Saved successfully")
        return
    
    def read_data(self, table: str, user_id: str):
        with self.__get_db_connector() as conn:
            df = pd.read_sql(f"SELECT * FROM {table} WHERE user_id = {user_id}", conn)
        return df
