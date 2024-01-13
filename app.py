#app.py

import streamlit as st
from utils import TextToSQLConverter, SQLQueryExecutor, TABLES_DICT

class StreamlitApp:
    def __init__(self, text_to_sql_converter, query_executor):
        self.text_to_sql_converter = text_to_sql_converter
        self.query_executor = query_executor

    def run(self):
        st.set_page_config(page_title="QnA Demo")
        st.header("Query Generator")

        input_text = st.text_input("Input: ", key="input")

        submit = st.button("Ask the question")

        if submit:
            # Generate SQL Query
            sql_query = self.text_to_sql_converter.inference(input_text, TABLES_DICT)

            # Execute SQL Query
            values = self.query_executor.execute_query(sql_query)

            # Display SQL Query and Result
            st.subheader("SQL Query:")
            st.write(sql_query)

            st.subheader("Result:")
            st.write(values)

if __name__ == "__main__":
    text_to_sql_converter = TextToSQLConverter()
    query_executor = SQLQueryExecutor()

    app = StreamlitApp(text_to_sql_converter, query_executor)
    #app.run()
