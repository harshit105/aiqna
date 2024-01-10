# Introduction
1. AQINA allows you to chat with uploaded PDF/CSV/TXT files using GPT functionalities.
2. The application intelligently breaks the document into smaller chunks and a semantic search is first performed on your file content and the most relevant answer is returned to the user.
3. Simple chat like UI

## Project Overview
- Approach
    There are three ways users can solve use cases with the help of LLMs on their custom data. Prompt engineering, embeddings, and fine-tuning. AQINA uses embeddings to answer queries.
    
    For making AQINA I’ve used the embeddings approach to retrieve information from documents using LLM. The documents are processed through a model that creates smaller chunks and generates embeddings of those chunks. These embeddings are stored in a vector database. When a user queries the LLM, the embeddings are retrieved from the vector store and used by the LLM to generate a response from the custom data.
    
    ![How embeddings work](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*bYy116KZAanbxXta4PCkjQ.png)

- Tech Stack
    - Front-end: HTML, CSS, JavaScript
    - Back-end: Flask, Python
    - Database: ChromaDB to store vector embeddings
    - Framework: Langchain

## UML
```mermaid
sequenceDiagram
    participant User
    participant System
    participant Infrastructure

    User->>System: Upload PDF/CSV/TXT

    System->>System: Files saved in memory
    System->>System: Read individual file using Loaders
    System->>System: Split text to chunks
    System->>System: Create hash of document
    System->>Infrastructure: Check hash of document
    Infrastructure->>System: Check if document already exists
    System->>System: If document exists, skip
    System->>System: If doesn't exist, create embedding
    System->>Infrastructure: Store embeddings in Vector store(Chromadb)
    System->>User: Return success

    User->>System: Ask Question
    System->>System: Load LLM
    Infrastructure->>System: Get embeddings
    System->>System: Build RetrievalQA chain to answer query
    System->>System: Run query
    System->>System: Process result and get source info
    System->>User: Return answer
```