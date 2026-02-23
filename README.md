# Music Discovery Engine

A technical desktop application designed for high-fidelity music discovery, leveraging semantic analysis to bridge the gap between natural language user intent and structured metadata.

## Technical Architecture
* **Semantic Metadata Mapping:** The engine utilizes a Large Language Model (LLM) reasoning layer to perform zero-shot classification. This allows the system to map unstructured user prompts into specific Last.fm genre tags without the need for static keyword dictionaries.
* **Hybrid Failover Logic:** Designed with a robust Graceful Degradation strategy. If the primary AI API is unreachable, the system automatically pivots to a local heuristic-based genre map to ensure continuous service availability.
* **Event-Driven Interface:** Developed using the Tkinter framework, the GUI manages an asynchronous event loop. It utilizes manual UI refreshes to maintain responsiveness during I/O-bound network requests to external REST APIs.
* **Data Persistence:** Integrated a session-based buffering system that allows users to export accumulated search results to a local flat-file format for permanent storage.

## Technology Stack
* **Language:** Python 3.10+
* **Intelligence Layer:** OpenAI API (GPT-4o-mini)
* **Data Source:** Last.fm REST API
* **GUI Framework:** Tkinter (Custom High-Contrast Dark Theme)
* **Security:** Environment variable isolation via python-dotenv

## System Execution
1. **Intent Processing:** The user provides a natural language description of a mood or atmosphere.
2. **Metadata Refinement:** The LLM extracts semantic themes and translates them into valid API parameters.
3. **Data Retrieval:** The application executes requests to the Last.fm API to fetch tracks and artists corresponding to the refined metadata.
4. **Session Export:** Search results are aggregated in the GUI buffer and can be appended to a local text file for future reference.

## Installation and Setup

**1. Install Dependencies:**
```bash
pip install requests python-dotenv openai
```

**2. Configure Environment:**
Create a `.env` file in the root directory with the following credentials (ensure `.env` is added to your `.gitignore`):
```env
LASTFM_API_KEY=your_lastfm_key
OPENAI_API_KEY=your_openai_key
```

**3. Launch Application:**
```bash
python gui.py
```