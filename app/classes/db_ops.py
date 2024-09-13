from dotenv import load_dotenv
load_dotenv()
import os
uri=os.getenv("DB_Connection_url")
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
class db_operations:
    """
        uuid
        student_id:
        first_name:
        last_name:
        date_of_birth:
        subject:
        marks:
        created_at:
        modified_at: Defined a function and trigger operation
    """
    def __init__(self,user_query):
        llm=ChatOpenAI(model="gpt-4o-mini")
        self.db = SQLDatabase.from_uri(os.getenv("DB_Connection_url"))
        chain = create_sql_query_chain(llm, self.db)
        self.response = chain.invoke({"question": user_query})
        self.user_query=user_query
    def rectify_read_query(self,response):
        select_index = response.find("SELECT")
        semicolon_index = response.find(";", select_index)
        if select_index != -1 and semicolon_index != -1:
            response=response[select_index:semicolon_index + 1]
            import re
            modified_query = re.sub(r'SELECT.*?FROM', 'SELECT * FROM', response, flags=re.DOTALL)
            return modified_query
        else:
            return None
    def rectify_update_query(self,response):
        select_index = response.find("UPDATE")
        semicolon_index = response.find(";", select_index)
        if select_index != -1 and semicolon_index != -1:
            return response[select_index:semicolon_index + 1]
        else:
            return None
    def rectify_insert_query(self,response):
        select_index = response.find("INSERT")
        semicolon_index = response.find(";", select_index)
        if select_index != -1 and semicolon_index != -1:
            return response[select_index:semicolon_index + 1]
        else:
            return None
    def rectify_delete_query(self,response):
        select_index = response.find("DELETE")
        semicolon_index = response.find(";", select_index)
        if select_index != -1 and semicolon_index != -1:
            return response[select_index:semicolon_index + 1]
        else:
            return None
    def ask_llm(self):
        template = """
            You are expert in answering the questions with truthful explanation \
            from the financial data.\
            Explain the data points how it is derived or formed use the meta data from\
            database {metadata}
            Give  me the concise explanation of the follwing user question\
            Answer from the user question strictly from the below user query\
            {context}
            """
        return PromptTemplate(input_variables=["context","metadata"], template=template)  
    def perform_db_operation(self):
        if "SELECT" in self.response:
            print(self.response)
            read_query=self.rectify_read_query(self.response)
            llm = ChatOpenAI(model="gpt-4", temperature=0)
            print(read_query)
            x=self.db.run(read_query)
            print(x)
            prompt_template = self.ask_llm()
            chain = LLMChain(llm=llm, prompt=prompt_template)
            report = chain.run({"context": self.user_query,"metadata":x})
            return report
        else:
            return "There is any other operation found apart from read,delete,update or insert so not executing query"
    @staticmethod
    def get_latest_record():
        ret_query="SELECT student_id, first_name, last_name, subject,marks FROM students_records ORDER BY edited_at DESC LIMIT 1;"
        db = SQLDatabase.from_uri(os.getenv("DB_Connection_url"))
        return db.run(ret_query)