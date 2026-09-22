from app.ai.request import DesignRequest
from app.ai.generator import generate_proposal
from app.ai.converter import proposal_to_design
from app.core.validate_design import validate_design


request = DesignRequest(
    prompt="Build a temperature monitoring system"
)

proposal = generate_proposal(request)

design = proposal_to_design(
    proposal,
    design_id="demo-001",
    name="Temperature Monitoring System",
)

print("\n=== DESIGN ===")
print(design.model_dump_json(indent=2))

print("\n=== VALIDATION ===")

for result in validate_design(design):
    print(result)
