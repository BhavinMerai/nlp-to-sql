#utils.py

import psycopg2
import pandas as pd
import time
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

TABLES_DICT = {
    "nifty50": ["date", "open", "high", "close", "low", "sma5", "ema5", "TRIMA5", "HT_TRENDLINE", "TYPPRICE", "SAR"],
    "niftybank": ["date", "open", "high", "close", "low", "sma10", "ema10", "TRIMA10", "HT_TRENDLINE", "TYPPRICE", "SAR"]
    }

class DatabaseManager:
    def __init__(self, dbname, user, password, host="localhost"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def create_database(self):
        # Connect to the default database
        conn = psycopg2.connect(f"host={self.host} dbname=postgres user={self.user} password={self.password}")
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # Terminate connections to the 'accounts' database
        '''cur.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = %s;
        """, (self.dbname,))
        '''

        cur.execute("DROP DATABASE IF EXISTS {}".format(self.dbname))
        # Wait for the database to be dropped
        while True:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.dbname,))
            exists = cur.fetchone()
            if not exists:
                break
            time.sleep(2)  # Wait for 1 second before checking again

        cur.execute("CREATE DATABASE {}".format(self.dbname))

        conn.close()

        # Connect to the 'nifty' database
        conn = psycopg2.connect(f"host={self.host} dbname={self.dbname} user={self.user} password={self.password}")
        cur = conn.cursor()

        return cur, conn

    def drop_tables(self, cur, conn, drop_table_queries):
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()

    def create_tables(self, cur, conn, create_table_queries):
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()

    @staticmethod
    def create_table_queries():
        return [
            """
            CREATE TABLE IF NOT EXISTS nifty50 (
                date TIMESTAMP PRIMARY KEY,
                open REAL,
                high REAL,
                close REAL,
                low REAL,
                sma5 REAL,
                ema5 REAL,
                TRIMA5 REAL,
                HT_TRENDLINE REAL,
                TYPPRICE REAL,
                SAR REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS niftybank (
                date TIMESTAMP PRIMARY KEY,
                open REAL,
                high REAL,
                close REAL,
                low REAL,
                sma10 REAL,
                ema10 REAL,
                TRIMA10 REAL,
                HT_TRENDLINE REAL,
                TYPPRICE REAL,
                SAR REAL
            )
            """
        ]

    def insert_data(self, cur, conn, table_name, insert_query, data):
        try:
            for i, row in data.iterrows():
                values = tuple(row[column] for column in TABLES_DICT[table_name])
                print("Inserting row:", values)
                cur.execute(insert_query, values)
                conn.commit()
            else:
                print("Data inserted into {} table.".format(table_name))
        except Exception as e:
            print("Error inserting data:", str(e))

class StockDataLoader:
    @staticmethod
    def load_csv(file_path):
        # Use pandas to load CSV into a DataFrame
        return pd.read_csv(file_path)

class TextToSQLConverter:
    def __init__(self, model_name="juierror/flan-t5-text2sql-with-schema-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def get_prompt(self, tables, question):
        prompt = f"""convert question and table into SQL query. tables: {tables}. question: {question}"""
        return prompt

    def prepare_input(self, question: str, tables: Dict[str, List[str]]):
        tables = [f"""{table_name}({",".join(tables[table_name])})""" for table_name in tables]
        tables = ", ".join(tables)
        prompt = self.get_prompt(tables, question)
        input_ids = self.tokenizer(prompt, max_length=512, return_tensors="pt").input_ids
        return input_ids

    def inference(self, question: str, tables: Dict[str, List[str]]) -> str:
        input_data = self.prepare_input(question=question, tables=tables)
        outputs = self.model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=512)
        result = self.tokenizer.decode(token_ids=outputs[0], skip_special_tokens=True)
        return result

class SQLQueryExecutor:
    def __init__(self, cur, conn):
        self.cur = cur
        self.conn = conn

    def execute_query(self, sql_query):
        self.cur.execute(sql_query)
        values = self.cur.fetchall()
        return values

