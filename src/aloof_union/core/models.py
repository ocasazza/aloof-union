# aloof_union/core/models.py
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class AutomationType(Enum):
    FRESHSERVICE = "freshservice"
    JSM = "jsm"
    MERMAID = "mermaid"


@dataclass
class Condition:
    field: str
    operator: str
    value: Any


@dataclass
class Action:
    type: str
    parameters: Dict[str, Any]


@dataclass
class Transition:
    from_state: str
    to_state: str
    conditions: List[Condition]
    actions: List[Action]


@dataclass
class WorkflowState:
    name: str
    description: Optional[str] = None
    is_initial: bool = False
    is_terminal: bool = False
    properties: Dict[str, Any] = None


@dataclass
class UnifiedWorkflow:
    states: Dict[str, WorkflowState]
    transitions: List[Transition]
    metadata: Dict[str, Any]
