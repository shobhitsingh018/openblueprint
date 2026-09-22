from typing import Literal

from pydantic import BaseModel


AIRole = Literal[
    "architecture",
    "engineering",
    "coding",
    "documentation",
]


class RoutingDecision(BaseModel):
    role: AIRole
    reason: str


def route_task(
    prompt: str,
    task_type: str = "auto",
) -> RoutingDecision:

    if task_type != "auto":
        return RoutingDecision(
            role=task_type,
            reason="Role explicitly selected by the user/request.",
        )

    text = prompt.lower()

    engineering_keywords = [
        "voltage", "current", "power", "sensor", "component",
        "interface", "circuit", "pcb", "motor", "mcu",
        "microcontroller", "datasheet", "tolerance",
        "electrical", "mechanical", "thermal",
    ]

    coding_keywords = [
        "code", "python", "c++", "c/c++", "firmware",
        "function", "script", "algorithm", "api", "debug",
        "software", "program",
    ]

    documentation_keywords = [
        "document", "documentation", "report", "manual",
        "readme", "bom", "specification",
    ]

    if any(word in text for word in coding_keywords):
        return RoutingDecision(
            role="coding",
            reason="Task contains software or implementation concepts.",
        )

    if any(word in text for word in engineering_keywords):
        return RoutingDecision(
            role="engineering",
            reason="Task contains engineering or hardware-specific concepts.",
        )

    if any(word in text for word in documentation_keywords):
        return RoutingDecision(
            role="documentation",
            reason="Task requests documentation or engineering artifacts.",
        )

    return RoutingDecision(
        role="architecture",
        reason="Task requires general system decomposition or architecture reasoning.",
    )
