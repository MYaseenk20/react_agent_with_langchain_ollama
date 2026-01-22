import os
from typing import Union, List

from dotenv import load_dotenv
from langchain_classic.agents.format_scratchpad import format_log_to_str
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description, Tool
from langchain_ollama import ChatOllama

from callback import AgentCallbackHandler

load_dotenv()

@tool
def get_text_length(text:str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip('"')
    return len(text)

def find_tool_by_name(tools : List[Tool],tool_name:str)-> Tool:
    for tool in tools:
        if tool.name.lower() == tool_name.strip().lower():
            return tool
    raise ValueError(f"Tool {tool_name} not found")


if __name__ == '__main__':
    print("Hello React Langchain")
    tools = [get_text_length]

    template = """
         Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),tool_names="".join([t.name for t in tools])
    )


    llm = ChatOllama(
        temperature=0.5,
        model="gemma2:latest",
        stop=["\nObservation",],
        callbacks=[AgentCallbackHandler()],
    )

    intermediate_step = []

    agent = {"input": lambda x:x["input"]} | {"agent_scratchpad": lambda x:format_log_to_str(x["agent_scratchpad"])} | prompt | llm | ReActSingleInputOutputParser()

    agent_step = None
    while True:
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {"input": "What is the length of 'Dog' in characters?", "agent_scratchpad": intermediate_step})

        if isinstance(agent_step, AgentFinish):
            print(f" Final Answer : {agent_step.return_values}")
            break

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools,tool_name)
            tool_input = agent_step.tool_input
            observation = tool_to_use.func(str(tool_input))
            intermediate_step.append((agent_step,str(observation)))



