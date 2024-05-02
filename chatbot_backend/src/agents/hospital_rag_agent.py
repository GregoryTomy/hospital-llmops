import os
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, create_openai_functions_agent, AgentExecutor
from langchain import hub
from chains.review_chain import reviews_vector_chain
from chains.cypher_chain import cypher_chain
from tools.wait_times import get_current_wait_times, get_shortest_wait_hospital


HOSPITAL_AGENT_MODEL = os.getenv("HOSPITAL_AGENT_MODEL")

# instead of defining an agent prompt from scratch, we load a predifined prompt from LangCahin Hub
hospital_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

# Create 4 tools for the agent
tools = [
    Tool(
        name="Experiences",
        func=reviews_vector_chain.invoke,
        description="""Function is useful when you need to an answer questions about
        patient experiences, feelings, or any other qualititative question that could
        be answered about a patient using semantic search. Not useful for answering
        objective questions that involve counting, percentages, aggregations, or listing
        facts. Use the entire prompt as input to the tool. For instance, if the prompt is
        "Are patients satisfied with their care?", the input should be "Are patients 
        satisfied with their care?". 
        """,
    ),
    Tool(
        name="Graph",
        func=cypher_chain.invoke,
        description="""Function is useful for answering questions about patients, 
        physicans, hospitals, insurance payers, patient review statistics, and hospital
        visit details. Use the entire prompt as input to the tool. For instance, if
        the prompt is "How many visits have there been?", the input should be "How many
        visits have there been?".
        """,
    ),
    Tool(
        name="Waits",
        func=get_current_wait_times,
        description="""Function should be used when asked about current wait times at a
        specific hospital. This tool can only get the current wait time at a hospital and
        does not have any information about aggregate or historical wait times. Do not pass
        the word "hospital" as input, only the hospital name itself. For example, if the prompt
        is "What is the current wait time at Jordan Inc Hopsital?", the input should be
        "Jordan Inc".
        """,
    ),
    Tool(
        name="Availabilty",
        func=get_shortest_wait_hospital,
        description="""Function used when you need to find out which hospital has the 
        shortest wait time. This tool does not have any information about aggregate or 
        historical wait times. This tool returns a dictionary with the hospital name as the
        key and the wait time in minutes as the value.
        """,
    ),
]

# instantiate open ai chat object
chat_model = ChatOpenAI(
    model=HOSPITAL_AGENT_MODEL,
    temperature=0,
)

# instantiate the agent
hospital_rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=hospital_agent_prompt,
    tools=tools,
)

# instantiate the runtime for the agent
hospital_rag_agent_executor = AgentExecutor(
    agent=hospital_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
