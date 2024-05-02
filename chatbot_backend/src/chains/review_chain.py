import os
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.prompts import (PromptTemplate,
                               SystemMessagePromptTemplate,
                               HumanMessagePromptTemplate,
                               ChatPromptTemplate,)

HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")

# Create a vector index in Neo4j. Every `Review` node will get an
# embedding property which is a vector representation of the existing
# node properties.
neo4j_vector_index = Neo4jVector.from_existing_graph(
    embedding=OpenAIEmbeddings(),
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="reviews",   # name of the vector index
    node_label="Review",    # node to create embeddings for
    text_node_properties= [
        "physician_name",
        "patient_name",
        "text",
        "hospital_name",
    ], # node properties to include in the embedding
    embedding_node_property="embedding" # name of the embedding node property
)

review_template = """Your job is to use patient reviews to answer questions
about their experience at a hosptial. Use the following context to answer
questions. Be as detailed as possible and don't make up any information
that's not from the context. If you do not know an answer, say you don't know.

{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"],
                          template=review_template)
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"],
                          template="{question}")
)

messages = [review_system_prompt, review_human_prompt]

# define overall prompt template that integrates both context and question variables
review_prompt = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages
)

# Set up a retrieval chain using the Neo4j vector index for fetching relevant reviews based on the question context.
# This is the retriever we will use
reviews_vector_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model=HOSPITAL_QA_MODEL, temperature=0),
    chain_type="stuff",   # pass all 12 reviews to the prompt
    retriever=neo4j_vector_index.as_retriever(k=12),    # return 12 review embeddings from a similarity search
)

reviews_vector_chain.combine_documents_chain.llm_chain.prompt = review_prompt