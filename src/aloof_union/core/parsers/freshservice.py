# aloof_union/parsers/freshservice.py
# from typing import Dict
from aloof_union.core.models import (
    Action,
    Condition,
    Transition,
    UnifiedWorkflow,
    WorkflowState,
)
from aloof_union.exceptions import ParserError

from .base import WorkflowParser


class FreshServiceParser(WorkflowParser):
    def parse(self, content: dict) -> UnifiedWorkflow:
        try:
            states = {}
            transitions = []

            # Parse states
            for state_name, state_data in content["states"].items():
                states[state_name] = WorkflowState(
                    name=state_name,
                    description=state_data.get("description"),
                    is_initial=state_data.get("is_initial", False),
                    is_terminal=state_data.get("is_terminal", False),
                    properties=state_data,
                )

            # Parse transitions
            for trans in content["transitions"]:
                conditions = [
                    Condition(c.get("field", ""), c.get("operator", ""), c.get("value"))
                    for c in trans.get("conditions", [])
                ]

                actions = [
                    Action(a.get("type", ""), a.get("parameters", {}))
                    for a in trans.get("actions", [])
                ]

                transitions.append(
                    Transition(
                        from_state=trans["from_state"],
                        to_state=trans["to_state"],
                        conditions=conditions,
                        actions=actions,
                    )
                )

            return UnifiedWorkflow(states, transitions, {"source": "freshservice"})

        except KeyError as e:
            raise ParserError(f"Missing required field in Fresh Service workflow: {e}")
        except Exception as e:
            raise ParserError(f"Error parsing Fresh Service workflow: {e}")

    def serialize(self, workflow: UnifiedWorkflow) -> dict:
        try:
            return {
                "states": {
                    state_name: {
                        "description": state.description,
                        "is_initial": state.is_initial,
                        "is_terminal": state.is_terminal,
                        **(state.properties or {}),
                    }
                    for state_name, state in workflow.states.items()
                },
                "transitions": [
                    {
                        "from_state": trans.from_state,
                        "to_state": trans.to_state,
                        "conditions": [
                            {"field": c.field, "operator": c.operator, "value": c.value}
                            for c in trans.conditions
                        ],
                        "actions": [
                            {"type": a.type, "parameters": a.parameters}
                            for a in trans.actions
                        ],
                    }
                    for trans in workflow.transitions
                ],
            }
        except Exception as e:
            raise ParserError(f"Error serializing to Fresh Service format: {e}")
