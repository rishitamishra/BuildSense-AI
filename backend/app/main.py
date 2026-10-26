import json, os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from .schemas import Analysis

load_dotenv()
app = FastAPI(title="Multimodal Construction Intelligence API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])

PROMPT = """Return only valid JSON with keys mode, summary, safety, cracks, planning, valuation, site_advice, limitations.
safety: {overall_risk, findings:[{issue,severity,evidence,recommended_action}]}
cracks: {observed,crack_type,severity,probable_causes:[],recommended_actions:[],disclaimer}
planning: {project_summary,estimated_duration_days,milestones:[],materials:[{item,quantity,estimated_cost_inr}],estimated_total_cost_inr}
valuation: {estimated_value_inr,assumptions:[],confidence,note}
site_advice: {advice:[],weather_note}. Be conservative, do not claim certainty from images, and do not invent live weather or property market data.
Clearly mark estimates as rough. For concerning hazards/cracks recommend qualified on-site review."""

def demo(description, project):
    area = float(project.get("built_up_area_sqft") or 1000)
    rate = float(project.get("cost_per_sqft_inr") or 1800)
    cost = max(0, area * rate)
    return {
      "mode":"demo","summary":"Demo-mode result. Add GEMINI_API_KEY to enable image-aware Gemini analysis.",
      "safety":{"overall_risk":"unknown","findings":[{"issue":"Site conditions require an on-site check","severity":"medium","evidence":"Demo mode does not inspect image contents.","recommended_action":"Have the site supervisor check PPE, edge protection, electrical safety and clear walkways."}]},
      "cracks":{"observed":False,"crack_type":"Not assessed in demo mode","severity":"unknown","probable_causes":["Image-aware analysis is not enabled."],"recommended_actions":["Upload clear context and close-up photos; arrange qualified inspection for concerning cracks."],"disclaimer":"This is not a structural diagnosis."},
      "planning":{"project_summary":description[:400] or "Construction project","estimated_duration_days":max(14,int(project.get("floors") or 1)*45),"milestones":["Site preparation","Foundation and structure","Services and finishing","Inspection and handover"],"materials":[{"item":"Indicative construction allowance","quantity":f"{area:g} sq ft","estimated_cost_inr":cost}],"estimated_total_cost_inr":cost},
      "valuation":{"estimated_value_inr":None,"assumptions":["No verified local comparable sales supplied."],"confidence":"low","note":"Add local comparable rates and consult a qualified valuer."},
      "site_advice":{"advice":["Keep walkways clear and documented.","Record hazards and corrective actions.","Verify quantities against approved drawings."],"weather_note":"Live weather is not connected; check a local forecast."},
      "limitations":["Demo mode does not analyze image contents.","Costs are illustrative, not a contractor quotation.","Not a substitute for a licensed engineer, safety officer or property valuer."]
    }

@app.get("/api/health")
def health():
    return {"status":"ok","gemini_configured":bool(os.getenv("GEMINI_API_KEY"))}

@app.post("/api/analyze", response_model=Analysis)
async def analyze(description: str = Form(""), project_data: str = Form("{}"), images: List[UploadFile] = File(default=[])):
    try:
        project = json.loads(project_data or "{}")
        if not isinstance(project, dict): raise ValueError("Expected a JSON object")
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(400, detail=f"Invalid project_data JSON: {exc}")
    key = os.getenv("GEMINI_API_KEY","").strip()
    if not key: return demo(description, project)
    parts = [types.Part.from_text(text=f"Project data: {json.dumps(project)}\nSite description: {description}")]
    for img in images:
        if not (img.content_type or "").startswith("image/"):
            raise HTTPException(400, detail=f"{img.filename} is not an image")
        raw = await img.read()
        if len(raw) > 10 * 1024 * 1024: raise HTTPException(413, detail=f"{img.filename} exceeds 10 MB")
        parts.append(types.Part.from_bytes(data=raw, mime_type=img.content_type))
    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),
            contents=[types.Content(role="user", parts=parts)],
            config=types.GenerateContentConfig(system_instruction=PROMPT, response_mime_type="application/json", temperature=0.2))
        data = json.loads(response.text)
        data["mode"] = "gemini"
        return Analysis.model_validate(data)
    except Exception as exc:
        print(f"Gemini analysis error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="AI analysis failed; check backend logs and API key/model configuration."
        ) from exc
