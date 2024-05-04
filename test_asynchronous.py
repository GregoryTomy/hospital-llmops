import time
import requests
import httpx
import asyncio

# CHATBOT_URL = "http://localhost:8000/hospital-rag-agent"
CHATBOT_URL = "https://ideal-adventure-67j6vprxvj7f4vv5-8000.app.github.dev/hospital-rag-agent"

questions = [
   "What is the current wait time at Wallace-Hamilton hospital?",
   "Which hospital has the shortest wait time?",
   "At which hospitals are patients complaining about billing and insurance issues?",
   "What is the average duration in days for emergency visits?",
   "What are patients saying about the nursing staff at Castaneda-Hardy?",
   "What was the total billing amount charged to each payer for 2023?",
   "What is the average billing amount for Medicaid visits?",
   "How many patients has Dr. Ryan Brown treated?",
   "Which physician has the lowest average visit duration in days?",
   "How many visits are open and what is their average duration in days?",
   "Have any patients complained about noise?",
   "How much was billed for patient 789's stay?",
   "Which physician has billed the most to cigna?",
   "Which state had the largest percent increase in Medicaid visits from 2022 to 2023?",
]

request_bodies = [{"text": question} for question in questions]

start_time = time.perf_counter()
outputs = [
    requests.post(CHATBOT_URL, json=data) for data in request_bodies
]
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds \n")

async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response

async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    outputs = [r.json()["output"] for r in responses]
    return outputs

request_bodies = [{"text": question} for question in questions]

start_time = time.perf_counter()
outputs = [
    requests.post(CHATBOT_URL, json=data) for data in request_bodies
]
end_time = time.perf_counter()

print(f"Run time async: {end_time - start_time} seconds \n")