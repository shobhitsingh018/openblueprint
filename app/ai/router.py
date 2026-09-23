from typing import Literal
from pydantic import BaseModel

AIRole = Literal["architecture", "engineering", "coding", "documentation"]


class RoutingDecision(BaseModel):
    role: AIRole
    reason: str


def route_task(prompt: str, task_type: str = "auto") -> RoutingDecision:
    if task_type != "auto":
        return RoutingDecision(role=task_type, reason="Role explicitly selected by the request.")
    text = prompt.lower()
    if any(x in text for x in ("code", "python", "c++", "firmware", "script", "algorithm", "debug", "api")):
        return RoutingDecision(role="coding", reason="Request contains software implementation concepts.")
    if any(x in text for x in ("voltage", "current", "power", "sensor", "component", "interface", "pcb", "motor", "mcu", "microcontroller", "datasheet", "circuit")):
        return RoutingDecision(role="engineering", reason="Request contains engineering-specific concepts.")
    if any(x in text for x in ("document", "report", "manual", "readme", "bom", "specification")):
        return RoutingDecision(role="documentation", reason="Request asks for documentation or artifacts.")
    return RoutingDecision(role="architecture", reason="Request requires system decomposition or architecture reasoning.")
