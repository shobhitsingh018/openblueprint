import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.ai.config import AIConfig
from app.ai.converter import proposal_to_design
from app.ai.parser import parse_proposal
from app.ai.request import DesignRequest
from app.ai.service import assess_proposal, generate_design_proposal
from app.ai.health import check_ollama
from app.core.design import Design
from app.core.engineering_rules import assess_design_status
from app.core.validate_design import validate_design

router = APIRouter(prefix="/api/v1")


@router.get("/")
def root_ui():
    return FileResponse("web/index.html")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.2.0"}


@router.get("/ai/health")
def ai_health() -> dict:
    return check_ollama()


@router.post("/design/propose")
def propose(request: DesignRequest) -> dict:
    try:
        proposal = generate_design_proposal(request, AIConfig(provider="ollama"))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"proposal": proposal.model_dump(), "assessment": assess_proposal(proposal)}


@router.post("/design/validate")
def validate(design: Design) -> dict:
    results = validate_design(design)
    status = assess_design_status(results)
    return {"valid": status == "VALID", "status": status, "results": results}


@router.post("/design/proposal-to-design")
def convert(request: dict) -> dict:
    if "proposal" not in request:
        raise HTTPException(status_code=400, detail="Missing 'proposal'.")
    try:
        parsed = parse_proposal(json.dumps(request["proposal"]))
        design = proposal_to_design(parsed, request.get("design_id", "design-001"),
                                    request.get("name", "Untitled Design"))
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    results = validate_design(design)
    return {"design": design.model_dump(), "status": assess_design_status(results), "results": results}
