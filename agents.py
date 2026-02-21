from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.getenv("CEREBRAS_API_KEY") or os.getenv("OPENAI_API_KEY"),
)

def research_agent(domain):
    prompt = f"""
    Analyze the company with domain: {domain}

    Return JSON:
    {{
      "industry": "",
      "growth_stage": "",
      "tech_focus": "",
      "possible_pain_points": [],
      "strategic_signals": {{
          "industry_match": true,
          "recent_funding": false,
          "ai_hiring": true,
          "automation_mentions": false,
          "expansion": true
      }}
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Research agent error: {e}")
        return {"industry": "", "growth_stage": "", "tech_focus": "", "strategic_signals": {}}


def strategy_agent(score, research_data):
    prompt = f"Based on score {score} and research {research_data}, should DataVex pursue this company? Give reasoning."
    try:
        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Strategy agent error: {e}")
        return f"Score {score}/100. Manual review recommended."


def outreach_agent(domain, reasoning):
    prompt = f"Write a personalized outreach email to the CTO of {domain} based on: {reasoning}"
    try:
        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Outreach agent error: {e}")
        return f"Hi, reaching out regarding {domain}. {reasoning}"