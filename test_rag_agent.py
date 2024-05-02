import dotenv
from chatbot.src.agents.hospital_rag_agent import hospital_rag_agent_executor


dotenv.load_dotenv()

response = hospital_rag_agent_executor.invoke(
    {"input": "What is the wait time at Wallace-Hamilton?"}
)

print(response.get("output"))

response = hospital_rag_agent_executor.invoke(
    {"input": "Which hospital has the shortest wait time?"}
)

print(response.get("output"))

response = hospital_rag_agent_executor.invoke(
    {"input": "What have patients said about their quality of rest during their stay?"}
)

print(response.get("output"))

response = hospital_rag_agent_executor.invoke(
    {"input": "Which physician has treated the most patients covered by Cigna?"}
)

print(response.get("output"))