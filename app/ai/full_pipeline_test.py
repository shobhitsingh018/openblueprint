from app.ai.config import AIConfig
from app.ai.converter import proposal_to_design
from app.ai.request import DesignRequest
from app.ai.service import generate_design_proposal
from app.core.validate_design import validate_design


request = DesignRequest(
    prompt="Build a temperature monitoring system"
)

config = AIConfig(
    provider="mock"
)

proposal = generate_design_proposal(
    request,
    config,
)

print("=== AI PROPOSAL ===")
print(proposal.model_dump_json(indent=2))

design = proposal_to_design(
    proposal,
    design_id="ai-demo-001",
    name="AI Temperature Monitoring System",
)

print("\n=== DESIGN ===")
print(design.model_dump_json(indent=2))

print("\n=== VALIDATION ===")

for result in validate_design(design):
    print(result)
