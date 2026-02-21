# DataVex Lead Intelligence Engine

Analyzes company domains and returns research, lead score, strategy, and outreach email using Cerebras LLM.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **API key**  
   Put your Cerebras API key in `.env`:
   ```
   CEREBRAS_API_KEY=your_key_here
   ```

## Run

**In VS Code:**  
1. Open this folder in VS Code.  
2. Press **F5** or go to **Run and Debug** and choose **"DataVex: Run server (frontend + backend)"**.  
3. Or use **Terminal → Run Task → Run DataVex server**.  
4. Open **http://127.0.0.1:8001** in your browser (or run task **"Open frontend in browser"**).

**Easiest (Windows):** Double-click **`run.bat`** — starts server and opens **http://127.0.0.1:8001**.

**From terminal:**
```bash
pip install -r requirements.txt
python start_server.py
```
Then open **http://127.0.0.1:8001** and enter a company domain (e.g. `stripe.com`) and click **Analyze**.

## API

- `GET /` – serves the frontend.
- `POST /analyze` – body: `{"domain": "example.com"}`. Returns industry, score, signals, reasoning, and outreach email.
