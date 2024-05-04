from fastapi import FastAPI
from pydantic import BaseModel
from agents.hospital_rag_agent import hospital_rag_agent_executor
from utils.async_utils import async_retry
from typing import List

class HospitalQueryInput(BaseModel):
    text: str


class HospitalQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: List[str]


app = FastAPI(
    title="Hospital Chatbot",
    description="Endpoints for a hospital system graph RAG chatbot",
)


@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """Asynchronously invokes the agent with retry logic

    Args:
        query (str): The query to be sent to the agent

    Returns:
        dict: Agent response
    """
    return await hospital_rag_agent_executor.ainvoke({"input": query})


@app.get("/")
async def get_status():
    """Return status of the server"""
    return {"status": "running"}


@app.post("/hospital-rag-agent")
async def query_hospital_agent(query: HospitalQueryInput) -> HospitalQueryOutput:
    """Queries the hospital RAG agent and returns the response

    Args:
        query (HospitalQueryInput): Input query for the RAG agent

    Returns:
        HospitalQueryOutput: Response output from the RAG agent.
    """
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
