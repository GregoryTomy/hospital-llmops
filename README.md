# Hospital Chatbot - LLMOps with LangChain and Neo4J


## Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Business scenario](#business-scenario)
- [Dataset](#dataset)
- [Chatbot Solution](#chatbot-solution)
- [Local Deployment](#local-deployment-guide)


## Demo
>The chatbot can be accessed at:
https://hospitalllm.azurewebsites.net/

## Business scenario
A large hospital system is seeking to enhance its ability to dynamically interact with and analyze vast amounts of patient, visit, physician, hospital, and insurance payer data. The goal is to develop a solution that enables non-technical stakeholders to obtain real-time insights through natural language queries, eliminating the need for expertise in SQL or reliance on data analysts for report generation and dashboard creation.

The stakeholders require answers to two primary types of questions, each demanding a different approach in query processing:

1. **Objective Queries**: These involve straightforward, quantifiable data retrieval such as calculating the total amount billed to a specific insurance provider within a given year. For example, stakeholders might ask, "What was the total amount billed to Blue Cross Blue Shield in the fiscal year 2023?" This type of question can typically be answered using predefined SQL queries, but creating new queries for each unique or nuanced question can be time-consuming and inefficient.
2. **Subjective Analysis**: These questions pertain to qualitative assessments and require parsing through narrative data sources like patient feedback. For instance, stakeholders might inquire, "What are the common themes in patient feedback regarding the cleanliness of the facilities?" or "How do patients describe their interactions with medical staff?" These queries necessitate advanced natural language processing capabilities to analyze sentiment, themes, and patterns within unstructured text data, providing a range of plausible insights rather than a single objective answer.

## Dataset

The datasets cover various aspects of hospital operations including details about hospitals, physicians, insurance payers, patient visits, and reviews. Find more details [here](data/README.md).

### Hospital Data Graph

![](images/hospital_graph_1.png)

## Chatbot Solution

![](images/chatbot_solution.png)

To address the complex needs of the hospital's stakeholders, our solution incorporates a chatbot powered by an LLM agent, leveraging LangChain and Neo4J. This setup allows us to efficiently handle both structured and unstructured queries, enhancing the hospital's ability to interact with and analyze its data. The chatbot solution consists of three primary components:

1. **Objective Query Processor using Cypher Queries**:
    - For objective, data-specific queries, we utilize a Cypher Chain - a GPT 3.5 model integrated within LangChain. This model takes user inputs in natural language and converts them into Cypher queries. These queries are directly run on Neo4J, a graph database that houses structured data about hospitals, physicians, patient visits, and more. This approach allows for rapid and accurate data retrieval without requiring stakeholders to learn SQL or other database querying languages.
2. **Semantic Analysis with Vector Search**:
    - For subjective analysis and semantic queries, we employ a vector search index built into Neo4J. This allows for advanced natural language processing directly on the graph. We store vector embeddings alongside the structured data in the knowledge graph. This integration enables stakeholders to perform semantic searches, such as understanding themes from patient feedback or analyzing sentiments about hospital services, directly through the chatbot.
3. **External Data Integration for Dynamic Information**:
    - Recognizing that not all required information resides within our internal databases, we integrate external data sources for real-time data retrieval. This component of the solution includes custom functions within LangChain that simulate dynamic information such as current wait times at various hospital locations or identify the facility with the shortest wait time. These functions simulate external API calls and are crucial for providing timely and relevant information to stakeholders.
    
## Local Deployment Guide

---
#### Acknowledgements
Special thanks to [Harrison Hoffman](https://www.linkedin.com/in/harrison-f-hoffman/) for his excellent guide and insights.