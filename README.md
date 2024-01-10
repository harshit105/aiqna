# aiqna
llm with custom vector embeddings

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