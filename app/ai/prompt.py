"""Prompt construction for design generation."""

import json

SYSTEM_PROMPT = """You are a senior systems engineer.
You output ONLY valid JSON that matches the provided schema.
Never invent fields. Never use markdown. Never add commentary.
Every object MUST have a unique, non-empty "id" string.
Every reference (component_ids, source, target, interface_ids) MUST point
to an id that was actually defined earlier in the same JSON document.
"""

SCHEMA_CONTRACT = """
Output a single JSON object with this exact shape:

{
  "requirements": [
    {"id": "REQ-1", "text": "..."}
  ],
  "systems": [
    {"id": "SYS-1", "name": "...", "component_ids": ["CMP-1"]}
  ],
  "components": [
    {"id": "CMP-1", "name": "...", "interfaces": [
        {"id": "IF-1", "name": "...", "type": "power|data|mechanical"}
    ]}
  ],
  "connections": [
    {"id": "CON-1", "source": "IF-1", "target": "IF-2"}
  ],
  "constraints": [
    {"id": "CONS-1", "text": "..."}
  ]
}

HARD RULES:
1. All ids are strings, unique across the ENTIRE document.
2. Prefer prefixed ids: REQ-, SYS-, CMP-, IF-, CON-, CONS-.
3. Every system.component_ids entry must exist in components[].id.
4. Every connection.source and connection.target must exist in
   some component's interfaces[].id.
5. Every component must define at least one interface.
6. requirements must contain at least one entry.
7. Do not wrap the JSON in ``` fences.
"""

FEW_SHOT = """
EXAMPLE (valid):

{
  "requirements": [
    {"id": "REQ-1", "text": "Provide 5V regulated output at 2A"}
  ],
  "systems": [
    {"id": "SYS-1", "name": "Power Supply", "component_ids": ["CMP-1", "CMP-2"]}
  ],
  "components": [
    {"id": "CMP-1", "name": "Buck Converter", "interfaces": [
      {"id": "IF-1", "name": "VIN", "type": "power"},
      {"id": "IF-2", "name": "VOUT", "type": "power"}
    ]},
    {"id": "CMP-2", "name": "Load", "interfaces": [
      {"id": "IF-3", "name": "VIN", "type": "power"}
    ]}
  ],
  "connections": [
    {"id": "CON-1", "source": "IF-2", "target": "IF-3"}
  ],
  "constraints": [
    {"id": "CONS-1", "text": "Input voltage 12V +/- 5%"}
  ]
}
"""


def build_design_prompt(user_description: str) -> str:
    return (
        f"{SCHEMA_CONTRACT}\n\n"
        f"{FEW_SHOT}\n\n"
        f"Now design the following. Output JSON only.\n\n"
        f"DESCRIPTION:\n{user_description}\n"
    )


def build_repair_prompt(raw_json: str, errors: list[str]) -> str:
    error_block = "\n".join(f"- {e}" for e in errors)
    return (
        "The following JSON failed validation. Fix ONLY the listed problems. "
        "Preserve everything else. Output corrected JSON only.\n\n"
        f"VALIDATION ERRORS:\n{error_block}\n\n"
        f"CURRENT JSON:\n{raw_json}\n"
    )