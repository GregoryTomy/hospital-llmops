import dotenv
from chatbot.src.chains.review_chain import reviews_vector_chain

dotenv.load_dotenv()

query = """What have patients said about hospital
efficiency? Mention details from specific reviews."""

response = reviews_vector_chain.invoke(query)

print(response.get("result"))

