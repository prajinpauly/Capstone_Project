from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
import json
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import StructuredTool
from langchain.schema import messages_to_dict
import pandas as pd
from collections import defaultdict
import sys

# Conversation memory setup
conversational_memory = ConversationBufferMemory(
    memory_key='chat_history',
    k=15,
    return_message=True
)

# LLM setup (update with your actual Azure OpenAI credentials)
llm = AzureChatOpenAI(
    deployment_name="tcs-gpt-4-32k", 
    model_name="gpt-3.5-turbo",
    openai_api_version="2024-02-01",
    openai_api_base="https://servicedeskgpt.openai.azure.com/",
    openai_api_key="1c9bfb8389c74ca0b9b0495d246bac6f",
    temperature=0, 
    max_tokens=256
)

# Updated tool for aged care/disability HRM
def aged_care_hrm_tool(query):
    """
    Always use this tool to answer the queries. Never use the Internet.
    You are an agent that asks users the queries given below in a step-by-step manner. Follow the instructions given below:

    Key points:
        - First greet the user when they greet you and start asking the questions from the same query.
        - If the user answers the current query, then ask the next question in the same conversation.
        - Only ask the questions given below. Do not ask questions from anywhere else.
        - After asking all the below questions efficiently just exit the compilation.

    Questions to ask:
        1. What is the name of your aged care or disability service?
        2. Can you describe the main services you provide?
        3. Who are your primary clients (e.g., elderly, people with disabilities)?
        4. What are the key HR challenges you face (e.g., staff shortages, training, compliance)?
        5. Are there specific regulatory requirements you must comply with (e.g., NDIS, Aged Care Quality Standards)?
        6. What systems do you currently use for HR management (e.g., rostering, payroll, training)?
        7. Do you have issues with staff retention or recruitment?
        8. What are your main concerns regarding staff training and qualifications?
        9. How do you currently track compliance and incident reporting?
        10. Are there any technology gaps in your current HRM processes?
        11. What is your preferred method for staff communication and updates?
        12. Do you require integration with existing HR or care management systems?
        13. What is your desired timeline for improving your HRM processes?
        14. Are there any key milestones or audits coming up?
        15. Is there any other information about your HRM needs or regulatory requirements?

    Important Instruction:
        - After asking all the 15 questions the AI must reply with - "Thank you for answering all the questions."
        - Never reply with sentences other than "Thank you for answering all the questions."
    """

    query_answer = f"""
        User: Hi!
        AI: Hello there! I will be asking some questions about your HRM and compliance needs in the aged care/disability sector. You can answer them one by one.
            Let's start: What is the name of your aged care or disability service?

        User: [User's answer]
        AI: Can you describe the main services you provide?

        User: [User's answer]
        AI: Who are your primary clients (e.g., elderly, people with disabilities)?

        User: [User's answer]
        AI: What are the key HR challenges you face (e.g., staff shortages, training, compliance)?

        User: [User's answer]
        AI: Are there specific regulatory requirements you must comply with (e.g., NDIS, Aged Care Quality Standards)?

        User: [User's answer]
        AI: What systems do you currently use for HR management (e.g., rostering, payroll, training)?

        User: [User's answer]
        AI: Do you have issues with staff retention or recruitment?

        User: [User's answer]
        AI: What are your main concerns regarding staff training and qualifications?

        User: [User's answer]
        AI: How do you currently track compliance and incident reporting?

        User: [User's answer]
        AI: Are there any technology gaps in your current HRM processes?

        User: [User's answer]
        AI: What is your preferred method for staff communication and updates?

        User: [User's answer]
        AI: Do you require integration with existing HR or care management systems?

        User: [User's answer]
        AI: What is your desired timeline for improving your HRM processes?

        User: [User's answer]
        AI: Are there any key milestones or audits coming up?

        User: [User's answer]
        AI: Is there any other information about your HRM needs or regulatory requirements?

        User: {query}
        AI:
    """
    return query_answer.format(query=query)

# Updated prompt for the agent
promptt = (
    "Always use the tool provided to answer the queries step by step for the aged care/disability industry HRM and compliance. "
    "Never skip using the tool. Never use the Internet."
)

# Main agent function
def get_agent_message(query):
    tools = [
        StructuredTool.from_function(aged_care_hrm_tool)
    ]
    agent = initialize_agent(
        tools,
        llm,
        max_iteration=3,
        memory=conversational_memory,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    # Add the updated prompt to the agent's prompt template
    agent.agent.llm_chain.prompt.template += promptt

    extracted_messages = conversational_memory.chat_memory.messages
    data = messages_to_dict(extracted_messages)
    whole_memory_list = json.loads(json.dumps(data))

    try:
        if len(whole_memory_list) > 1:
            if "Thank you for answering all the questions" in whole_memory_list[-1]['data']['content']:
                f_dict = defaultdict(list)
                n = len(whole_memory_list)
                print(whole_memory_list)
                print()
                for dictt in whole_memory_list:
                    print(dictt['data']['type'], dictt['data']['content'])
                    print()
                    key = dictt['data']['type']
                    value = dictt['data']['content']
                    f_dict[key].append(value)
                df = pd.DataFrame.from_dict(data=f_dict)
                print(df)
                df.to_csv('aged_care_hrm_answers.csv', index=False)
                exit()
    except Exception as e:
        print("Error:", e)
        return {
            "answer": "",
            "memory": whole_memory_list
        }

    answer = agent.run(query)

    extracted_messages = conversational_memory.chat_memory.messages
    data = messages_to_dict(extracted_messages)
    whole_memory_list = json.loads(json.dumps(data))

    return {
        "answer": answer,
        "memory": whole_memory_list
    }

# Example usage:
# result = get_agent_message("Hi!")
# print(result["answer"])
    
