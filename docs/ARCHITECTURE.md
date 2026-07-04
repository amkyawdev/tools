# System Architecture & Workflow

```
flowchart TD
    A[User] --> B{Input Channel}
    B --> C[Telegram Bot]
    B --> D[Web UI - Next.js]
    B --> E[CLI Tool]
    B --> F[Voice Input]
    C --> G[Python Backend - FastAPI]
    D --> G
    E --> G
    F --> H[ElevenLabs TTS/STT] --> G
    G --> I[AI Brain Skills Framework]
    I --> J[Context Orchestrator]
    J --> K[Load Memory & Knowledge]
    K --> L[(Neon DB)]
    K --> M[(Qdrant Cloud)]
    I --> N[Select Domain Skills]
    N --> O{Task Type?}
    O -- Code --> P[Code Generator]
    O -- Docs --> Q[Doc Generator]
    O -- Export --> R[Data Exporter]
    O -- Package --> S[ZIP Packager]
    P --> T[OpenRouter LLM]
    P --> U[NVIDIA NIM]
    Q --> T
    R --> L
    S --> V[Generate ZIP]
    I --> W[Hooks System]
    W --> X[Pre/Post Processing]
    X --> Y[(Aiven Kafka)]
    V --> Z[Prepare Output]
    T --> Z
    U --> Z
    Q --> Z
    R --> Z
    Z --> AA{Output Channel}
    AA --> C
    AA --> D
    AA --> E
    D --> AB[Display in Chat]
    AB --> AC[Syntax Highlighting]
    AB --> AD[Download Links]
    C --> AE[Send Files]
    AE --> AF[Code File]
    AE --> AG[Doc File]
    AE --> AH[ZIP Archive]
    AE --> AI[Data File]
    Z --> AJ[Update Memory]
    AJ --> L
    AJ --> M
    Y --> AK[(Aiven OpenSearch)]
    AK --> AL[Dashboard Analytics]
```

## Architecture Layers

| Layer | Component | Technology |
|---|---|---|
| Input | Web UI, Telegram, CLI, Voice | Next.js, Telegram API, Python CLI, ElevenLabs |
| Orchestration | AI Brain Skills Framework | FastAPI + Python |
| AI Services | LLM, Embedding, TTS | OpenRouter, NVIDIA NIM, ElevenLabs |
| Memory | Short-term + Long-term | Neon PostgreSQL, Qdrant Vector DB |
| Streaming | Events & Analytics | Aiven Kafka + OpenSearch |
| Output | Code, Docs, ZIP, Data | Telegram, Web UI, CLI |
