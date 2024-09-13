# #  def read_record(self,params):
# #         """
# #         read operation or fetch record
# #         """
# #         key_value=None
# #         for x in params:
# #             if params[x]!="N/A":
# #                 key_value=x
# #         if key_value==None:
# #             return None
# #         else:
# #             response_1 = supabase.table("students_records").select("*").eq(key_value, params[key_value]).execute()
# #         return response_1
# from langchain.chains import create_sql_query_chain
# from langchain_community.utilities import SQLDatabase
# from langchain_openai import ChatOpenAI
# def rectify_query(response):
#     select_index = response.find("INSERT")
#     semicolon_index = response.find(";", select_index)
#     if select_index != -1 and semicolon_index != -1:
#         return response[select_index:semicolon_index + 1]
#     else:
#         return None
# llm = ChatOpenAI(model="gpt-4o-mini")
# db = SQLDatabase.from_uri("postgresql://postgres.xtwrxwsfdxociyuqhclx:tEMP_DATABASE217@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
# chain = create_sql_query_chain(llm, db)
# response = chain.invoke({"question": "Add a score of 90 for Jane Doe in Math"})
# sql_query=rectify_query(response)
# print(sql_query)
# db.run(sql_query)


# def read_record(self,user_quey):
        
        
        
    #     sql_query=self.rectify_query(response)
    #     return db.run(sql_query)
    # def insert_and_update_record(self,user_query):
    #     """
    #     Update operation 
    #     """
    #     from langchain.chains import create_sql_query_chain
    #     from langchain_community.utilities import SQLDatabase
    #     from langchain_openai import ChatOpenAI
    #     llm = ChatOpenAI(model="gpt-4o-mini")
    #     db = SQLDatabase.from_uri("postgresql://postgres.xtwrxwsfdxociyuqhclx:tEMP_DATABASE217@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
    #     chain = create_sql_query_chain(llm, db)
    #     response = chain.invoke({"question": user_query})
    #     sql_query=self.rectify_query(response)
    #     return db.run(sql_query)

    # def delete_record(self,user_query):
    #     """
    #     delete operation or delete record
    #     """
    #     from langchain.chains import create_sql_query_chain
    #     from langchain_community.utilities import SQLDatabase
    #     from langchain_openai import ChatOpenAI
    #     llm = ChatOpenAI(model="gpt-4o-mini")
    #     db = SQLDatabase.from_uri("postgresql://postgres.xtwrxwsfdxociyuqhclx:tEMP_DATABASE217@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
    #     chain = create_sql_query_chain(llm, db)
    #     response = chain.invoke({"question": user_query})
    #     sql_query=self.rectify_query(response)
    #     return db.run(sql_query)
    #     pass