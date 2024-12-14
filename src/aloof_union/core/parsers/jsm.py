# aloof_union/parsers/jsm.py
# from typing import Dict, List
from aloof_union.core.models import (
    Action,
    Condition,
    Transition,
    UnifiedWorkflow,
    WorkflowState,
)
from aloof_union.exceptions import ParserError

from .base import WorkflowParser


class JSMParser(WorkflowParser):
    def parse(self, content: dict) -> UnifiedWorkflow:
        try:
            states = {}
            transitions = []

            # Parse JSM statuses to states
            for status in content.get("statuses", []):
                properties = {
                    "statusCategory": status.get("statusCategory", "TO_DO"),
                    "jsmId": status.get("id"),
                    "jsmType": status.get("statusType"),
                }

                states[status["name"]] = WorkflowState(
                    name=status["name"],
                    description=status.get("description"),
                    is_initial=status.get("initial", False),
                    is_terminal=status.get("statusCategory") == "DONE",
                    properties=properties,
                )

            # Parse JSM rules to transitions
            for rule in content.get("rules", []):
                conditions = []
                for jsm_condition in rule.get("conditions", []):
                    conditions.append(
                        Condition(
                            field=jsm_condition.get("field", {}).get("name", ""),
                            operator=jsm_condition.get("operator", ""),
                            value=jsm_condition.get("value"),
                        )
                    )

                actions = []
                for post_function in rule.get("postFunctions", []):
                    actions.append(
                        Action(
                            type=post_function.get("type", ""),
                            parameters=post_function.get("configuration", {}),
                        )
                    )

                transitions.append(
                    Transition(
                        from_state=rule["fromStatus"],
                        to_state=rule["toStatus"],
                        conditions=conditions,
                        actions=actions,
                    )
                )

            return UnifiedWorkflow(states, transitions, {"source": "jsm"})

        except KeyError as e:
            raise ParserError(f"Missing required field in JSM workflow: {e}")
        except Exception as e:
            raise ParserError(f"Error parsing JSM workflow: {e}")

    def serialize(self, workflow: UnifiedWorkflow) -> dict:
        try:
            return {
                "statuses": [
                    {
                        "name": state.name,
                        "description": state.description,
                        "initial": state.is_initial,
                        "statusCategory": state.properties.get(
                            "statusCategory", "TO_DO"
                        ),
                        "id": state.properties.get("jsmId"),
                        "statusType": state.properties.get("jsmType"),
                    }
                    for state in workflow.states.values()
                ],
                "rules": [
                    {
                        "fromStatus": trans.from_state,
                        "toStatus": trans.to_state,
                        "conditions": [
                            {
                                "field": {"name": c.field},
                                "operator": c.operator,
                                "value": c.value,
                            }
                            for c in trans.conditions
                        ],
                        "postFunctions": [
                            {"type": a.type, "configuration": a.parameters}
                            for a in trans.actions
                        ],
                    }
                    for trans in workflow.transitions
                ],
            }
        except Exception as e:
            raise ParserError(f"Error serializing to JSM format: {e}")
