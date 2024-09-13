import json
import openai
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field, conint, validator
from typing import Sequence,Optional,List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from dotenv import load_dotenv
load_dotenv()
from langchain.chains import create_tagging_chain_pydantic
class dboperation(BaseModel):
    create_record:Optional[str]=Field("N/A",enum=["YES","NO"], description="Indicates whether a database new record creation operation should be performed.")
    read_record:Optional[str]=Field("N/A",enum=["YES","NO"], description="Specifies whether information should be retrieved from the database")
    update_record:Optional[str]=Field("N/A",enum=["YES","NO"], description="Indicates for a update operation or mpdifying existing operation should be performed on the database")
    delete_record:Optional[str]=Field("N/A",enum=["YES","NO"], description="Specifies whether an information deletion operation should be executed on the database")

class db_schema(BaseModel):
    operation:Sequence[dboperation] = Field("N/A",description ="Identify the kind of operation professor want to perform in database")
    student_id:Optional[int] = Field ("N/A",description="Unique student id e.g 1234, 923456 etc")
    first_name:Optional[str] =Field ("N/A",description="First name of the student")
    last_name:Optional[str] = Field ("N/A",description="Last Name of the student")
    subject:Optional[str] = Field ("N/A", enum=["Physics","Math","Chemistry"],description="Identify the subject")
    marks:Optional[int] = Field("N/A",description="Marks in a particular subject e.g 27 ,62 ,99 etc")
class db_query_designing:
    def __init__(self, model_name, max_tokens, temperature, n,query):
        self.llm_1 = ChatOpenAI(
            openai_api_key=openai.api_key,
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            n=n
        )
        self.query = query
    def identify_operation(self):
        llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
        chain = create_tagging_chain_pydantic(dboperation, llm)
        x=chain.run(self.query)
        print(x)
        return x

    def extract_first_json_block(self,text):
        stack = []
        start_index = None
        end_index = None
        for i, char in enumerate(text):
            if char == '{':
                if not stack:
                    start_index = i
                stack.append(char)
            elif char == '}':
                if stack:
                    stack.pop()
                    if not stack:
                        end_index = i
                        break
        if start_index is not None and end_index is not None:
            json_block = text[start_index:end_index + 1]
            return json_block
        else:
            return None

    def info_extract(self, text):
        parser = PydanticOutputParser(pydantic_object=db_schema)
        format_instructions = parser.get_format_instructions()
        template_sys = f"""You are an expert in finding key information from the professor's instruction \
            and what kind of operation professor want to perform in database\
            so find the meaningfull information from the given instruction\ \
            Find meaningful information as per the given structured format \
            - First: Analyze the instruction query. \
            - Second: Find one kind of operation professor want to perform \
            - third : Extract the meaninful information as per the schema \
            - Final task: Carefully describe and validate the information using the provided data.
        """

        template_assistant = """Give me the answer, I'm going to format it with the JSON schema \
        I know the metadata so I will enhance the quality of extraction"""
        template = """
        Use the following format:
        {format_instructions}
        {text}
        YOUR ANSWER:
        """
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(template_sys),
                AIMessagePromptTemplate.from_template(template_assistant),
                HumanMessagePromptTemplate.from_template(template)
            ],
            input_variables=["text"],
            partial_variables={"format_instructions": format_instructions}
        )

        _input = prompt.format_prompt(text=text)
        output = self.llm_1(_input.to_messages())
        if "```json" in output.content:
            json_string=self.extract_first_json_block(output.content)
        else:
            json_string = output.content
        return json.loads(json_string)
    def post_process(self,json_string):
        operation_dict = json_string.get('operation', [{}])[0]
        remaining_dict = {k: v for k, v in json_string.items() if k != 'operation'}
        return operation_dict, remaining_dict

if __name__=="__main__":
    query="Summarize all student scores in Physics."
    model_name = "gpt-4o"
    max_tokens = 2000
    temperature = 0
    n = 1
    obj=db_query_designing(model_name, max_tokens, temperature, n,query)
    y=obj.info_extract(query)
    operation_dict, remaining_dict =obj.post_process(y)
    print(f"Operation dict is:{operation_dict}")
    print(f"remaining dict is:{remaining_dict}")