#main.py

from utils import DatabaseManager, TextToSQLConverter, SQLQueryExecutor, StockDataLoader
from app import StreamlitApp

# Database configuration
DB_NAME = "nifty"
DB_USER = "postgres"
DB_PASSWORD = "admin"

def main():
    # Read data
    Nifty50 = StockDataLoader.load_csv(r"C:\Users\BMERAI\OneDrive - Capgemini\Desktop\work-folder\dataset\stock_market\NIFTY 50_with_indicators_.csv")
    NiftyBank = StockDataLoader.load_csv(r"C:\Users\BMERAI\OneDrive - Capgemini\Desktop\work-folder\dataset\stock_market\NIFTY BANK_with_indicators_.csv")

    #Limiting data records
    Nifty50_10r = Nifty50.head(10)
    NiftyBank_10r = NiftyBank.head(10) 
    # Drop table queries
    drop_table_queries = ["DROP TABLE IF EXISTS nifty50", "DROP TABLE IF EXISTS niftybank"]

    # Database operations
    db_manager = DatabaseManager(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur, conn = db_manager.create_database()
    db_manager.drop_tables(cur, conn, drop_table_queries)

    # Create tables
    Nifty50TableInsert = """INSERT INTO nifty50 (
        date, open, high, close, low, sma5, ema5, TRIMA5, HT_TRENDLINE, TYPPRICE, SAR
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    NiftyBankTableInsert = """INSERT INTO niftybank (
        date, open, high, close, low, sma10, ema10, TRIMA10, HT_TRENDLINE, TYPPRICE, SAR
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    table_queries = db_manager.create_table_queries()

    db_manager.create_tables(cur, conn, table_queries)
    db_manager.insert_data(cur, conn, "nifty50", Nifty50TableInsert, Nifty50_10r)
    db_manager.insert_data(cur, conn, "niftybank", NiftyBankTableInsert, NiftyBank_10r)

    # Streamlit App
    app = StreamlitApp(TextToSQLConverter(), SQLQueryExecutor(cur, conn))
    app.run()

if __name__ == "__main__":
    main()

