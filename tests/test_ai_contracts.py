import json
from app.ai.parser import parse_proposal
from app.ai.proposal import DesignProposal
from app.ai.service import generate_design_proposal
from app.ai.config import AIConfig
from app.ai.request import DesignRequest
from app.ai.provider import AIProvider


def test_parser_rejects_extra_fields():
    payload = {"summary":"x", "unexpected":True}
    try:
        parse_proposal(json.dumps(payload))
    except ValueError:
        return
    raise AssertionError("Strict proposal parser accepted an extra field")


class StagedProvider(AIProvider):
    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str, response_schema=None) -> str:
        self.calls += 1
        if self.calls == 1:
            return json.dumps({
                "summary": "Two-stage architecture",
                "requirements": [{"id": "r", "description": "make a connected system"}],
                "components": [
                    {"id": "a", "name": "Source", "category": "sensor", "interfaces": [{"id": "a-out", "name": "OUT", "type": "data", "direction": "output"}]},
                    {"id": "b", "name": "Sink", "category": "controller", "interfaces": [{"id": "b-in", "name": "IN", "type": "data", "direction": "input"}]},
                ],
                "assumptions": [], "warnings": []
            })
        return json.dumps({
            "connections": [{"id": "c", "name": "Data", "source": "a-out", "target": "b-in", "interface_type": "data"}],
            "assumptions": [], "warnings": []
        })


def test_staged_ollama_path_builds_canonical_structure(monkeypatch):
    provider = StagedProvider()
    monkeypatch.setattr("app.ai.service.create_provider", lambda config: provider)
    proposal = generate_design_proposal(
        DesignRequest(prompt="make a connected system"),
        AIConfig(provider="ollama", model="local", refinement_passes=1),
    )
    assert isinstance(proposal, DesignProposal)
    assert proposal.systems and proposal.components and proposal.connections
    assert proposal.connections[0].source == "a-out"
    assert provider.calls == 2


def test_staged_path_rejects_unknown_connection_endpoint(monkeypatch):
    class BadProvider(StagedProvider):
        def generate(self, prompt: str, response_schema=None) -> str:
            if self.calls == 0:
                super().generate(prompt, response_schema)
                return json.dumps({
                    "summary": "Bad",
                    "requirements": [{"id": "r", "description": "x"}],
                    "components": [{"id": "a", "name": "A", "interfaces": [{"id": "a-out", "name": "OUT", "type": "data", "direction": "output"}]}],
                    "assumptions": [], "warnings": []
                })
            self.calls += 1
            return json.dumps({"connections": [{"id": "c", "source": "not-an-interface", "target": "a-out"}], "assumptions": [], "warnings": []})

    provider = BadProvider()
    monkeypatch.setattr("app.ai.service.create_provider", lambda config: provider)
    try:
        generate_design_proposal(DesignRequest(prompt="make a connected system"), AIConfig(provider="ollama", model="local"))
    except ValueError as exc:
        assert "unknown interface IDs" in str(exc)
        return
    raise AssertionError("Invalid connection endpoint was silently repaired")


def test_parser_rejects_alias_drift():
    payload = {
        "summary": "Alias drift",
        "status": "PROPOSED",
        "requirements": [{"id": "r", "description": "measure temperature"}],
        "systems": [],
        "components": [{
            "id": "c",
            "name": "Microcontroller",
            "manufacturer_part_number": "UNO",
        }],
        "connections": [],
        "constraints": [],
        "resources": [],
        "assumptions": [],
        "warnings": [],
    }
    try:
        parse_proposal(json.dumps(payload))
    except ValueError:
        return
    raise AssertionError("Parser accepted a non-contract field alias")


def test_staged_architecture_normalizes_small_model_structural_omissions(monkeypatch):
    from app.ai.staged_pipeline import generate_staged_proposal

    class LooseProvider(AIProvider):
        def __init__(self):
            self.calls = 0

        def generate(self, prompt: str, response_schema=None) -> str:
            self.calls += 1
            if self.calls == 1:
                return json.dumps({
                    "summary": "Temperature monitoring architecture",
                    "requirements": [
                        "A microcontroller capable of reading the temperature sensor and controlling the display.",
                        "A temperature sensor that can communicate with the microcontroller.",
                    ],
                    "components": [
                        {"name": "Microcontroller", "interfaces": [
                            {"id": "mcu-if-temp-sensor", "type": "i2c", "direction": "bidirectional"},
                            {"id": "mcu-if-display", "type": "spi", "direction": "output"},
                            {"id": "mcu-if-power", "type": "power", "direction": "input"},
                        ]},
                        {"name": "Temperature Sensor", "interfaces": [
                            {"id": "temp-if-mcu", "type": "i2c", "direction": "bidirectional"},
                            {"id": "temp-if-power", "type": "power", "direction": "input"},
                        ]},
                    ],
                    "assumptions": [], "warnings": []
                })
            return json.dumps({
                "connections": [
                    {"id": "c1", "source": "mcu-if-temp-sensor", "target": "temp-if-mcu", "interface_type": "i2c"}
                ],
                "assumptions": [], "warnings": []
            })

    provider = LooseProvider()
    monkeypatch.setattr("app.ai.service.create_provider", lambda config: provider)
    proposal = generate_design_proposal(
        DesignRequest(prompt="temperature monitoring"),
        AIConfig(provider="ollama", model="local"),
    )
    assert proposal.components[0].id == "microcontroller"
    assert proposal.components[0].interfaces[0].name == "I2C Interface"
    assert proposal.requirements[0].id == "req-001"
    assert proposal.connections[0].source == "mcu-if-temp-sensor"


def test_staged_connection_normalizes_component_interface_pairs(monkeypatch):
    from app.ai.staged_pipeline import generate_staged_proposal

    class PairProvider(AIProvider):
        def __init__(self):
            self.calls = 0

        def generate(self, prompt: str, response_schema=None) -> str:
            self.calls += 1
            if self.calls == 1:
                return json.dumps({
                    "summary": "Temperature architecture",
                    "requirements": ["Measure temperature"],
                    "components": [
                        {"name": "Microcontroller", "interfaces": [
                            {"id": "mcu-temp", "name": "Temperature bus", "type": "i2c", "direction": "bidirectional"}
                        ]},
                        {"name": "Temperature Sensor", "interfaces": [
                            {"id": "sensor-temp", "name": "Sensor bus", "type": "i2c", "direction": "bidirectional"}
                        ]},
                    ],
                    "assumptions": [], "warnings": []
                })
            return json.dumps({
                "connections": [{
                    "component_id": "microcontroller",
                    "interface_id": "mcu-temp",
                    "component_id_target": "temperature-sensor",
                    "interface_id_target": "sensor-temp",
                    "interface_type": "i2c",
                }],
                "assumptions": [{"reason": "I2C used for sensor communication."}],
                "warnings": [{"reason": "No electrical limits were specified."}],
            })

    provider = PairProvider()
    monkeypatch.setattr("app.ai.service.create_provider", lambda config: provider)
    proposal = generate_design_proposal(
        DesignRequest(prompt="temperature monitoring"),
        AIConfig(provider="ollama", model="local"),
    )
    assert proposal.connections[0].id == "conn-001"
    assert proposal.connections[0].source == "mcu-temp"
    assert proposal.connections[0].target == "sensor-temp"
    assert proposal.assumptions and "I2C used" in proposal.assumptions[0]
    assert proposal.warnings and "electrical limits" in proposal.warnings[0]


def test_staged_connection_rejects_mismatched_component_interface_pair(monkeypatch):
    from app.ai.staged_pipeline import generate_staged_proposal

    class PairProvider(AIProvider):
        def __init__(self):
            self.calls = 0

        def generate(self, prompt: str, response_schema=None) -> str:
            self.calls += 1
            if self.calls == 1:
                return json.dumps({
                    "summary": "Test",
                    "requirements": [],
                    "components": [
                        {"name": "A", "interfaces": [{"id": "a-if", "name": "A", "type": "data"}]},
                        {"name": "B", "interfaces": [{"id": "b-if", "name": "B", "type": "data"}]},
                    ],
                    "assumptions": [], "warnings": []
                })
            return json.dumps({"connections": [{
                "component_id": "a",
                "interface_id": "b-if",
                "component_id_target": "b",
                "interface_id_target": "b-if",
            }]})

    provider = PairProvider()
    monkeypatch.setattr("app.ai.service.create_provider", lambda config: provider)
    try:
        generate_design_proposal(
            DesignRequest(prompt="test"),
            AIConfig(provider="ollama", model="local"),
        )
    except ValueError as exc:
        assert "does not belong to component" in str(exc)
        return
    raise AssertionError("Mismatched component/interface pair was accepted")
