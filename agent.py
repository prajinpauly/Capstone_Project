from langchain.agents import Tool, initialize_agent,AgentType
from langchain.llms import OpenAI
import json
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool,StructuredTool
from langchain.schema import messages_from_dict,messages_to_dict
import pandas as pd
import csv
from collections import defaultdict
import sys


conversational_memory=ConversationBufferMemory(
    memory_key='chat_history',
    k=15,
    return_message=True
)
llm = AzureChatOpenAI(
    deployment_name="tcs-gpt-4-32k", 
    model_name="gpt-3.5-turbo",
    openai_api_version="2024-02-01",
    openai_api_base="https://servicedeskgpt.openai.azure.com/",
    openai_api_key= "1c9bfb8389c74ca0b9b0495d246bac6f" ,
    temperature=0, 
    max_tokens = 256)






def message_tool_old(query):

    """
    Always use this tool to answer the queries. Never use the Internet.
    You are an agent that asks users the queries given below in a step-by-step manner. Follow the instructions given below:

    Key points:
        - First greet the user when they greet you and start asking the questions from the same query.
        - If the user answers the current query, then ask the next question in the same conversation.
        - Only ask the questions given below. Do not ask questions from anywhere else.
        - After asking all the below questions efficiently just exit the compilation.

    Questions to ask:
        1. What is the name of your project?
        2. Can you provide a brief description of your project goals?
        3. Who is the primary audience or user group for this project?
        4. What are the key characteristics or demographics of your target audience?
        5. Do you have any specific design styles or themes in mind (e.g., modern, minimalist, colorful)?
        6. Are there any examples of designs you like that we can use as inspiration?
        7. What are the key features or functionalities you need for this project?
        8. Do you need this design to be optimized for specific devices (e.g., mobile, desktop, tablet)?
        9. Does your project need to follow an existing brand identity (e.g., logo, colors, typography)?
        10. If yes, can you upload or provide links to your branding assets?
        11. What is your desired deadline for the project?
        12. Are there any key milestones or checkpoints you’d like us to adhere to?
        13. Are there any technical requirements or constraints we need to consider (e.g., platforms, tools, or frameworks)?
        14. Do you have a preferred format for deliverables (e.g., PDFs, design files, code, etc.)?
        15. Is there any other information you’d like us to know about your project?

         
           
    
    Example interaction:
        User: Hi!
        AI: Hello there! I will be asking some questions about your project, and you can answer them one by one.
            Let’s start: What is the name of your project?

        User: The name of the project is RAG chatbot.
        AI: Can you provide a brief description of your project goals?
        
        User: The goals are to create an LLM chatbot to answer project-related queries.
    
        
    Important Instruction:
        - After asking all the 15 questions the AI must reply with - "Thank you for answering all the questions. "
        - Never reply with sentences other than "Thank you for answering all the questions."


    """
    query_answer=f"""
        User: Hi !
        AI : Hellow there. I will be asking some questions about the project and you have to answer it.
             What is the name of your project?

        User: The name of project is RAG chatbot .
        AI: Can you provide a brief description of your project goals?
        User: The goals are to make the project based on LLM chatbot to answer the queries . The queries will will be some questions aboutn the project.

        User : {query}
        AI : 


    """
    return query_answer.format(query)

def message_tool_new(query):

    """
    A tool for asking project-related questions sequentially.
    Always use this tool for answering user queries step by step.

    Key points:
        - First greet the user when they greet you and start asking the questions from the same query.
        - If the user answers the current query, then ask the next question in the same conversation.
        - Only ask the questions given below. Do not ask questions from anywhere else.

    Questions to ask:
        1. What is the name of your project?
        2. Can you provide a brief description of your project goals?
        3. Who is the primary audience or user group for this project?
        4. What are the key characteristics or demographics of your target audience?
        5. Do you have any specific design styles or themes in mind (e.g., modern, minimalist, colorful)?
        6. Are there any examples of designs you like that we can use as inspiration?
        7. What are the key features or functionalities you need for this project?
        8. Do you need this design to be optimized for specific devices (e.g., mobile, desktop, tablet)?
        9. Does your project need to follow an existing brand identity (e.g., logo, colors, typography)?
        10. If yes, can you upload or provide links to your branding assets?
        11. What is your desired deadline for the project?
        12. Are there any key milestones or checkpoints you’d like us to adhere to?
        13. Are there any technical requirements or constraints we need to consider (e.g., platforms, tools, or frameworks)?
        14. Do you have a preferred format for deliverables (e.g., PDFs, design files, code, etc.)?
        15. Is there any other information you’d like us to know about your project?    
    
    Example interaction:
        User: Hi!
        AI: Hello there! I will be asking some questions about your project, and you can answer them one by one.
            Let’s start: What is the name of your project?

        User: The name of the project is RAG chatbot.
        AI: Can you provide a brief description of your project goals?
        User: The goals are to create an LLM chatbot to answer project-related queries.

        
    """
    query_answer=f"""
        User: Hi !
        AI : Hellow there. I will be asking some questions about the project and you have to answer it.
             What is the name of your project?

        User: The name of project is RAG chatbot .
        AI: Can you provide a brief description of your project goals?
        User: The goals are to make the project based on LLM chatbot to answer the queries . The queries will will be some questions aboutn the project.

        User : {query}
        AI : 


    """
    return query_answer.format(query)




""" 
IF YOU ARE USING "message_tool_old" USE THE promptt as: 
promptt = "Never use the Internet to answer the question. Always use the tool provided to answer the questions in step by step manner."


IF YOU ARE USING "message_tool_new" CHANGE THE promptt as:
promptt ="\nAlways use the tool provided to answer the queries step by step. Never skip using the tool."
""" 






def get_agent_message(query):
    
    promptt = "\nNever use the Internet to answer the question. Always use the tool provided to answer the questions in step by step manner."

    
    tools=[
        StructuredTool.from_function(message_tool_old)
    ]
    agent=initialize_agent(tools,llm,max_iteration=3,memory=conversational_memory,agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,verbose=True,handle_parsing_errors=True)
    
    
    
    
    agent.agent.llm_chain.prompt.template+=promptt


    extracted_messages=conversational_memory.chat_memory.messages
    data=messages_to_dict(extracted_messages)
    whole_memory_list=json.loads(json.dumps(data))

    try:

        if len(whole_memory_list)>1:
        
            if "Thank you for answering all the questions" in whole_memory_list[-1]['data']['content']:


                f_dict=defaultdict(list)
                n=len(whole_memory_list)
                print(whole_memory_list)
                print()
                for dictt in whole_memory_list :
                    print(dictt['data']['type'],dictt['data']['content'])
                    print()
                    key=dictt['data']['type']
                    value=dictt['data']['content']
                    f_dict[key].append(value)

                    
                

                df=pd.DataFrame.from_dict(data=f_dict)
                print(df)
                df.to_csv('all_answers.csv',index=False)
                exit()
    except:
        return {
        "answer":"",
        "memory":whole_memory_list
    }
            

    answer=agent.run(query)
    

    extracted_messages=conversational_memory.chat_memory.messages
    data=messages_to_dict(extracted_messages)
    whole_memory_list=json.loads(json.dumps(data))
    
    
        



    return {
        "answer":answer,
        "memory":whole_memory_list
    }

    