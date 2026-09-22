from typing import Any
from pydantic import BaseModel, Field

from app.core.requirement import Requirement
from app.core.system import System
from app.core.component import Component
from app.core.connection import Connection
from app.core.resource import Resource
from app.core.constraint import Constraint


class Design(BaseModel):
    id: str
    name: str
    description: str = ""
    version: str = "0.1.0"

    requirements: list[Requirement] = Field(default_factory=list)
    systems: list[System] = Field(default_factory=list)
    components: list[Component] = Field(default_factory=list)
    connections: list[Connection] = Field(default_factory=list)

    constraints: list[Constraint] = Field(default_factory=list)
    resources: list[Resource] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)

    validation: dict[str, Any] = Field(default_factory=dict)
    simulation: dict[str, Any] = Field(default_factory=dict)

    bom: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
