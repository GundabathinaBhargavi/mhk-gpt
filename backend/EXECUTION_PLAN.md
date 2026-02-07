# Simple Execution Plan for MHK-GPT

Follow these steps faithfully to run the chatbot.

## 1. Prerequisites
*   **Docker Desktop**: Must be installed and running.
*   **Python (3.10+)**: Must be installed.

## 2. Start the Database
Open your terminal (Command Prompt/Terminal) and run this command:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

**⚠️ IMPORTANT:** Keep this terminal window **OPEN**. Do not close it.

## 3. Setup the Backend
Open a **NEW** terminal window and navigate to this folder (`MHK-GPT`).

1.  **Install Dependencies:**
    ```bash
    make install
    ```
    *(If 'make' is not available, run: `pip install -r backend/requirements.txt`)*

2.  **Setup Configuration:**
    *   Make sure you have a file named `.env` in the `backend/` folder.
    *   If not, copy `.env.example` and rename it to `.env`.
    *   **CRITICAL:** Open `.env` and paste your `OPENAI_API_KEY`.

## 4. Run the Server
In the same terminal where you installed dependencies, run:

```bash
make run
```
*(If 'make' is not available, run: `cd backend && python -m uvicorn app.main:app --reload`)*

Wait until you see: `Application startup complete`.

## 5. How to Use
1.  Open your browser and go to: **[http://localhost:8000/docs](http://localhost:8000/docs)**
2.  **Upload a Document:**
    *   Click `POST /api/v1/documents/upload` -> **Try it out**.
    *   Select a file (PDF, DOCX, etc.).
    *   Click **Execute**.
3.  **Chat with your Data:**
    *   Click `POST /api/v1/chat` -> **Try it out**.
    *   **Important:** Clear the `history` list so it looks like `[]` (or leave it empty).
    *   Type your question in `query`.
    *   Click **Execute**.
