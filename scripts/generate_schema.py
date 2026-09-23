import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.core.design import Design

schema = Design.model_json_schema()
schema.update({
    "$id": "https://openblueprint.dev/schemas/design.schema.json",
    "title": "OpenBlueprint Design",
    "description": "Canonical machine-readable representation of an OpenBlueprint engineering design.",
})
(root / "schemas" / "design.schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
print("Wrote schemas/design.schema.json")
