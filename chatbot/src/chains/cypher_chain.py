import os
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate

HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")
HOSPTIAL_CYPHER_MODEL = os.getenv("HOSPITAL_CYPHER_MODEL")

# Neo4jGraph allows LLMs to execute queries to Neo4j
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# sync any recent changes to the Neo4j instance
graph.refresh_schema()


#####################################################################
# Prompt Engineering
#####################################################################

# we provide specific instructions on what the LLM should and shouldn't do when generatin
# Cypher queries. Importantly, we show the LLM our graph's structure with the `schema` parameter
# we also provide some example queries and the categorical values of a few node properties.

cypher_generation_template = """
Task:
Generate Cypher query for Neo4j graph database

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your repsponses.
Do not respond to any questions that might ask anything other than for you to construct a Cypher statement.
Do not include any text expect the generated Cypher statement. 
Make sure the direction of the relationship is correct in your queries.
Make sure you alias both entities and relationships properly.
Do not run any queries that would add to or delete from the database.
Make sure to alias all statements that follow as with statement (e.g. WITH v as visit, c.billing_amount as billing_amount)
If you need to divide numbers, make sure to filter the denominator to be non zero.

Examples:
# who is the oldest patient and how old are they?
MATCH (p:Patient)
RETURN p.name AS oldest_patient,
        duration.between(date(p.dob), date()).years AS age

# which physician has billed the least to Cigna
MATCH (p:Payer) <- [c:COVERED_BY] - (v:Visit) - [t:TREATS] - (phy:Physician)
WHERE p.name = 'Cigna'
RETURN phy.name AS physician_name, SUM(c.billing_amount) AS total_billed
ORDER BY total_billed
LIMIT 1

# Which state had the largest percent increase in Cigna visits
# from 2022 to 2023?
MATCH (h:Hospital)<-[:AT]-(v:Visit)-[:COVERED_BY]->(p:Payer)
WHERE p.name = 'Cigna' AND v.admission_date >= '2022-01-01' AND
v.admission_date < '2024-01-01'
WITH h.state_name AS state, COUNT(v) AS visit_count,
     SUM(CASE WHEN v.admission_date >= '2022-01-01' AND
     v.admission_date < '2023-01-01' THEN 1 ELSE 0 END) AS count_2022,
     SUM(CASE WHEN v.admission_date >= '2023-01-01' AND
     v.admission_date < '2024-01-01' THEN 1 ELSE 0 END) AS count_2023
WITH state, visit_count, count_2022, count_2023,
     (toFloat(count_2023) - toFloat(count_2022)) / toFloat(count_2022) * 100
     AS percent_increase
RETURN state, percent_increase
ORDER BY percent_increase DESC
LIMIT 1

# How many non-emergency patients in North Carolina have written reviews?
match (r:Review)<-[:WRITES]-(v:Visit)-[:AT]->(h:Hospital)
where h.state_name = 'NC' and v.admission_type <> 'Emergency'
return count(*)

String category values:
Test results are on of: 'Inconclusive', 'Normal', 'Abnormal'
Visit statuses are one of: 'OPEN', 'DISCHARGED'
Admission Types are one of: 'Elective', 'Emergency', 'Urgent'
Payer names are one of: 'Cigna', 'Blue Cross', 'UnitedHealthCare', 'Medicare', 'Aetna'

A visit is considered open if its status is 'OPEN' and the discharge date is missing.

Use abbreviations when filtering on hospital states (e.g. "Texas" is "TX", "Colorado" is "CO", "North Carolina" is "NC", "Florida" is "FL", "Georgia" is "GA, etc.)

Make sure to use IS NULL or IS NOT NULL when analyzing missing properties.
Never return embedding properties in your queries. You must never include the statement "GROUP BY" in your query. 
Make sure to alias all statements that follow as with statement (e.g. WITH v as visit, c.billing_amount as
billing_amount)

The question is:
{question}
"""

qa_generation_template = """
You are an assistant that uses results from a Neo4j Cypher query to provide human-readable 
responses. The query results you receive are based on a user's question and are considered 
accurate. You should not question or correct this information. Your response should sound like 
a response to the user's question.

Query Results:
{context}

Question:
{question}

If the query results are empty (i.e., []), simply state that you do not know the answer.

If there are results:
- Provide an answer using the results.
- If the question relates to time, treat the results as being in days unless stated otherwise.
- Handle names carefully. For example, 'Jones, Brown and Murray' should be treated as a single entity. Ensure that lists of names are clear and unambiguous.

Always use the available data to answer the question, showing all relevant information. 
Never claim to lack the right information if data is provided.

Helpful Answer:
"""

# generate prompts
cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)

qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"], template=qa_generation_template
)

cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(model=HOSPTIAL_CYPHER_MODEL, temperature=0),
    qa_llm=ChatOpenAI(model=HOSPITAL_QA_MODEL, temperature=0),
    graph=graph,
    verbose=True,   # prints intermediate steps of the chain
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,   # cypher query inspected for errors and corrected before running
    top_k=100,
)

