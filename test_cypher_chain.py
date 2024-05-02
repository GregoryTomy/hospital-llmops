import dotenv

dotenv.load_dotenv()

from chatbot.src.chains.cypher_chain import cypher_chain

question = """What is the average visit duration for emergency visits in 
North Carolina?"""

print("\n")
print("Running Cypher query chain test....")
print(f"Question: {question}")

response = cypher_chain.invoke(question)

print(response.get("result"))
print("\n")