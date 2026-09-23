import json
from pathlib import Path
import jsonschema
from app.ai.config import AIConfig
from app.ai.converter import proposal_to_design
from app.ai.proposal import DesignProposal, ProposalComponent, ProposalConnection, ProposalInterface, ProposalRequirement, ProposalSystem
from app.ai.request import DesignRequest
from app.ai.service import generate_design_proposal
from app.core.engineering_rules import assess_design_status
from app.core.validate_design import validate_design


def test_mock_pipeline_produces_canonical_design():
    proposal = generate_design_proposal(DesignRequest(prompt="Build a temperature monitoring system"), AIConfig(provider="mock", refinement_passes=0))
    design = proposal_to_design(proposal, "demo-001", "Temperature Monitoring System")
    assert design.requirements and design.components and design.connections
    assert assess_design_status(validate_design(design)) == "VALID"


def test_zero_values_are_preserved():
    p = DesignProposal(summary="Zero", requirements=[ProposalRequirement(id="r", description="zero", measurable=True, target=0, min=0, max=0, unit="V")], components=[ProposalComponent(id="c", name="C", interfaces=[ProposalInterface(id="i", name="P", voltage_min=0)])])
    d = proposal_to_design(p, "d", "Zero")
    assert d.requirements[0].target_value == 0 and d.components[0].interfaces[0].voltage_min == 0


def test_connection_validation_uses_interface_ids():
    p = DesignProposal(summary="Connected", requirements=[ProposalRequirement(id="r", description="connect")], systems=[ProposalSystem(id="s", name="S", component_ids=["a", "b"])], components=[ProposalComponent(id="a", name="A", interfaces=[ProposalInterface(id="ia", name="OUT", type="data")]), ProposalComponent(id="b", name="B", interfaces=[ProposalInterface(id="ib", name="IN", type="data")])], connections=[ProposalConnection(id="c", source="ia", target="ib")])
    d = proposal_to_design(p, "d", "Connected")
    assert not any(r["rule_id"] == "CONNECTION-003" and r["status"] == "ERROR" for r in validate_design(d))


def test_duplicate_ids_are_rejected():
    p = DesignProposal(summary="Duplicate", requirements=[ProposalRequirement(id="same", description="A")], components=[ProposalComponent(id="same", name="B", interfaces=[ProposalInterface(id="i", name="I")])])
    assert any(r["rule_id"] == "DESIGN-003" and r["status"] == "ERROR" for r in validate_design(proposal_to_design(p, "d", "Duplicate")))


def test_incomplete_design_is_detected():
    p = DesignProposal(summary="Incomplete", requirements=[ProposalRequirement(id="r", description="A")], components=[ProposalComponent(id="c", name="Controller")])
    results = validate_design(proposal_to_design(p, "d", "Incomplete"))
    assert assess_design_status(results) == "INCOMPLETE"
    assert any(r["rule_id"] == "DESIGN-004" for r in results)


def test_complete_design_is_valid():
    p = DesignProposal(summary="Complete", requirements=[ProposalRequirement(id="r", description="Move data")], systems=[ProposalSystem(id="s", name="Main", component_ids=["a", "b"])], components=[ProposalComponent(id="a", name="Source", interfaces=[ProposalInterface(id="ia", name="OUT", type="data")]), ProposalComponent(id="b", name="Sink", interfaces=[ProposalInterface(id="ib", name="IN", type="data")])], connections=[ProposalConnection(id="c", source="ia", target="ib", interface_type="data")])
    assert assess_design_status(validate_design(proposal_to_design(p, "d", "Complete"))) == "VALID"


def test_canonical_schema_matches_design_dump():
    schema = json.loads((Path(__file__).parents[1] / "schemas" / "design.schema.json").read_text())
    p = DesignProposal(summary="Schema", requirements=[ProposalRequirement(id="r", description="A")])
    jsonschema.validate(proposal_to_design(p, "d", "Schema").model_dump(), schema)


def test_ollama_provider_uses_exact_json_schema(monkeypatch):
    from app.ai.ollama_provider import OllamaProvider
    from app.ai.proposal import DesignProposal

    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": DesignProposal(summary="ok").model_dump_json()}

    def fake_post(url, json, timeout):
        captured.update(json)
        return FakeResponse()

    import app.ai.ollama_provider as module
    monkeypatch.setattr(module.httpx, "post", fake_post)

    schema = DesignProposal.model_json_schema()
    OllamaProvider(model="qwen3:8b").generate("test", response_schema=schema)

    assert captured["format"] == schema
    assert captured["stream"] is False
