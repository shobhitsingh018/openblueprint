"""Deterministic normalization of raw AI output before validation."""

from __future__ import annotations
import re
from typing import Any


_ID_RE = re.compile(r"^[A-Za-z0-9_\-]+$")


def _coerce_id(value: Any, prefix: str, index: int) -> str:
    if isinstance(value, str) and value.strip() and _ID_RE.match(value.strip()):
        return value.strip()
    return f"{prefix}-AUTO-{index}"


def _dedupe_ids(items: list[dict], prefix: str) -> None:
    seen: set[str] = set()
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        new_id = _coerce_id(item.get("id"), prefix, i)
        if new_id in seen:
            new_id = f"{new_id}-{i}"
        item["id"] = new_id
        seen.add(new_id)


def normalize_proposal(raw: dict) -> dict:
    """Make raw AI output safe for the Design model + validator."""
    if not isinstance(raw, dict):
        raw = {}

    raw.setdefault("requirements", [])
    raw.setdefault("systems", [])
    raw.setdefault("components", [])
    raw.setdefault("connections", [])
    raw.setdefault("constraints", [])

    for key in ("requirements", "systems", "components",
                "connections", "constraints"):
        if not isinstance(raw[key], list):
            raw[key] = []

    # Drop non-dict entries
    for key in ("requirements", "systems", "components",
                "connections", "constraints"):
        raw[key] = [x for x in raw[key] if isinstance(x, dict)]

    # Assign unique IDs
    _dedupe_ids(raw["requirements"], "REQ")
    _dedupe_ids(raw["systems"], "SYS")
    _dedupe_ids(raw["components"], "CMP")
    _dedupe_ids(raw["connections"], "CON")
    _dedupe_ids(raw["constraints"], "CONS")

    # Normalize component interfaces
    all_interface_ids: set[str] = set()
    for ci, comp in enumerate(raw["components"]):
        ifaces = comp.get("interfaces")
        if not isinstance(ifaces, list):
            ifaces = []
        ifaces = [x for x in ifaces if isinstance(x, dict)]
        _dedupe_ids(ifaces, f"IF")
        for ii, iface in enumerate(ifaces):
            if iface["id"] in all_interface_ids:
                iface["id"] = f"{iface['id']}-{ci}-{ii}"
            all_interface_ids.add(iface["id"])
        comp["interfaces"] = ifaces
        comp.setdefault("name", f"Component {ci+1}")

    # Guarantee at least one interface per component
    for ci, comp in enumerate(raw["components"]):
        if not comp["interfaces"]:
            auto_id = f"IF-AUTO-{ci}"
            comp["interfaces"] = [
                {"id": auto_id, "name": "default", "type": "data"}
            ]
            all_interface_ids.add(auto_id)

    # Fix systems -> component refs
    valid_component_ids = {c["id"] for c in raw["components"]}
    for sys_ in raw["systems"]:
        refs = sys_.get("component_ids")
        if not isinstance(refs, list):
            refs = []
        sys_["component_ids"] = [r for r in refs if r in valid_component_ids]
        sys_.setdefault("name", sys_["id"])

    # Fix connections -> interface refs
    cleaned_conns = []
    for conn in raw["connections"]:
        src = conn.get("source")
        tgt = conn.get("target")
        if src in all_interface_ids and tgt in all_interface_ids and src != tgt:
            cleaned_conns.append(conn)
    raw["connections"] = cleaned_conns

        # Guarantee at least one requirement (correct field name is `description`)
    if not raw["requirements"]:
        raw["requirements"] = [
            {"id": "REQ-AUTO-0", "description": "Design as described by the user."}
        ]

    # DesignProposal requires `summary`
    raw.setdefault("summary", "AI-generated design proposal.")

        # Strip unknown top-level keys so Pydantic's strict validation passes
    allowed_top = {
        "summary", "status", "requirements", "systems", "components",
        "connections", "constraints", "resources", "assumptions", "warnings",
    }
    for k in list(raw.keys()):
        if k not in allowed_top:
            raw.pop(k)

    # Ensure `status` is one of the allowed literals
    if raw.get("status") not in ("PROPOSED", "APPROVED", "REJECTED", "APPLIED"):
        raw["status"] = "PROPOSED"

        # --- Field-name remapping (AI drift) ---
    # Requirements: `text` -> `description`
    for req in raw["requirements"]:
        if "description" not in req and "text" in req:
            req["description"] = req.pop("text")
        req.setdefault("description", "")

    # Constraints: `text` -> `description`, ensure `name`
    for cons in raw["constraints"]:
        if "description" not in cons and "text" in cons:
            cons["description"] = cons.pop("text")
        cons.setdefault("description", "")
        cons.setdefault("name", str(cons.get("id", "Constraint")))
        cons.setdefault("severity", "ERROR")

    # Components: ensure `category` exists
    for comp in raw["components"]:
        comp.setdefault("category", "unknown")

    # Connections: ensure `name` exists
    for conn in raw["connections"]:
        conn.setdefault("name", "")
    return raw