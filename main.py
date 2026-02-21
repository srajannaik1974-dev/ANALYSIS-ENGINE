from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from models import CompanyRequest
from agents import research_agent, strategy_agent, outreach_agent
from scoring import calculate_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend page (embedded so "/" always shows the input form no matter where the app runs)
FRONTEND_HTML = """<!DOCTYPE html>
<html>
<head>
<title>DataVex Lead Intelligence</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { margin:0; font-family:Arial; background:#f3f4f6; }
header { background:#2563eb; color:white; padding:20px; text-align:center; }
.container { max-width:1000px; margin:auto; padding:20px; }
input { padding:10px; width:70%; border-radius:6px; border:1px solid #ccc; }
button { padding:10px 15px; border:none; background:#2563eb; color:white; border-radius:6px; cursor:pointer; }
.card { background:white; padding:20px; margin-top:20px; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.05); }
.badge { background:#dcfce7; color:#166534; padding:5px 10px; border-radius:20px; margin-right:5px; display:inline-block; }
.score { font-size:40px; font-weight:bold; }
</style>
</head>
<body>
<header><h1>DataVex Lead Intelligence Engine</h1></header>
<div class="container">
<input type="text" id="domain" placeholder="Enter company domain">
<button onclick="analyze()">Analyze</button>
<div class="card"><h3>Overview</h3><p><strong>Industry:</strong> <span id="industry"></span></p><p><strong>Growth Stage:</strong> <span id="growth"></span></p><p><strong>Tech Focus:</strong> <span id="tech"></span></p></div>
<div class="card"><h3>Lead Score</h3><div class="score" id="score"></div><p id="verdict"></p></div>
<div class="card"><h3>Signals</h3><div id="signals"></div></div>
<div class="card"><h3>Reasoning</h3><p id="reasoning"></p></div>
<div class="card"><h3>Email</h3><p><strong>Subject:</strong> <span id="email_subject"></span></p><p id="email_body"></p></div>
</div>
<script>
async function analyze() {
    const domain = document.getElementById("domain").value;
    if(!domain){ alert("Enter company domain"); return; }
    const response = await fetch("/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ domain }) });
    const result = await response.json();
    if (result.error) {
        document.getElementById("verdict").innerText = result.error;
        return;
    }
    document.getElementById("industry").innerText = result.industry || "";
    document.getElementById("growth").innerText = result.growth_stage || "";
    document.getElementById("tech").innerText = result.tech_focus || "";
    document.getElementById("score").innerText = result.score ?? "";
    document.getElementById("verdict").innerText = result.verdict || "";
    document.getElementById("signals").innerHTML = (Array.isArray(result.signals) ? result.signals : []).map(s => '<span class="badge">'+s+'</span>').join("");
    document.getElementById("reasoning").innerText = result.reasoning || "";
    document.getElementById("email_subject").innerText = result.email_subject || "";
    document.getElementById("email_body").innerText = result.email_body || "";
}
</script>
</body>
</html>"""


def _signals_to_list(signals: dict) -> list:
    """Turn strategic_signals dict into list of active signal names for frontend."""
    names = []
    for key, val in (signals or {}).items():
        if val:
            names.append(key.replace("_", " ").title())
    return names


@app.get("/api/status")
def api_status():
    """Backend status (so tools that expect this still work)."""
    return {"message": "DataVex AI Backend Running with Cerebras"}


@app.get("/", response_class=HTMLResponse)
def serve_index():
    """Serve the frontend (input form) at root."""
    return HTMLResponse(FRONTEND_HTML)


@app.post("/analyze")
def analyze_company(request: CompanyRequest):
    try:
        domain = request.company_domain
        # 1. Get Research Data
        research = research_agent(domain)
        # 2. Extract signals and calculate score
        signals = research.get("strategic_signals", {})
        score = calculate_score(signals)
        # 3. Generate Strategy and Email
        strategy = strategy_agent(score, research)
        email = outreach_agent(domain, strategy)
        # Build response to match frontend expectations
        signals_list = _signals_to_list(signals)
        verdict = "Worth pursuing." if score >= 50 else "Lower priority."
        return {
            "industry": research.get("industry", ""),
            "growth_stage": research.get("growth_stage", ""),
            "tech_focus": research.get("tech_focus", ""),
            "score": score,
            "verdict": verdict,
            "signals": signals_list,
            "reasoning": strategy,
            "email_subject": "Partnership opportunity",
            "email_body": email,
        }
    except Exception as e:
        print(f"Backend Error: {e}")
        return {"error": str(e)}