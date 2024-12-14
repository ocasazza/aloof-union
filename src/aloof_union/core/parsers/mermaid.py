# aloof_union/parsers/mermaid.py
from typing import List, Tuple

from aloof_union.core.models import (  # Action,
    Condition,
    Transition,
    UnifiedWorkflow,
    WorkflowState,
)
from aloof_union.exceptions import ParserError

from .base import WorkflowParser


class MermaidParser(WorkflowParser):
    def _parse_transition_line(self, line: str) -> Tuple[str, str, List[str]]:
        """Parse a Mermaid transition line into components."""
        try:
            # Split on arrow
            parts = line.split("-->")
            if len(parts) != 2:
                raise ParserError(f"Invalid transition line: {line}")

            from_state = parts[0].strip()

            # Split destination and label
            to_parts = parts[1].split(":")
            to_state = to_parts[0].strip()

            # Parse conditions if they exist
            conditions = []
            if len(to_parts) > 1:
                label = to_parts[1].strip()
                conditions = [cond.strip() for cond in label.split("&&")]

            return from_state, to_state, conditions

        except Exception as e:
            raise ParserError(f"Error parsing Mermaid transition: {e}")

    def parse(self, content: str) -> UnifiedWorkflow:
        try:
            states = {}
            transitions = []
            current_note = None
            current_state = None

            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if not line or line.startswith("stateDiagram"):
                    continue

                # Handle state declarations
                if line.startswith("state"):
                    parts = line.split('"')
                    if len(parts) >= 3:
                        state_name = parts[1]
                        states[state_name] = WorkflowState(name=state_name)

                # Handle notes
                elif line.startswith("note"):
                    current_note = []
                    if "of" in line:
                        current_state = line.split("of")[1].strip()
                elif line == "end note" and current_note and current_state:
                    if current_state in states:
                        states[current_state].description = "\n".join(current_note)
                    current_note = None
                    current_state = None
                elif current_note is not None:
                    current_note.append(line)

                # Handle transitions
                elif "-->" in line:
                    from_state, to_state, condition_strs = self._parse_transition_line(
                        line
                    )

                    # Handle initial and terminal states
                    if from_state == "[*]":
                        if to_state in states:
                            states[to_state].is_initial = True
                        continue
                    if to_state == "[*]":
                        if from_state in states:
                            states[from_state].is_terminal = True
                        continue

                    # Create states if they don't exist
                    for state in (from_state, to_state):
                        if state not in states:
                            states[state] = WorkflowState(name=state)

                    # Create transition
                    conditions = [
                        Condition("condition", "equals", cond)
                        for cond in condition_strs
                    ]

                    transitions.append(
                        Transition(
                            from_state=from_state,
                            to_state=to_state,
                            conditions=conditions,
                            actions=[],
                        )
                    )

            return UnifiedWorkflow(states, transitions, {"source": "mermaid"})

        except Exception as e:
            raise ParserError(f"Error parsing Mermaid diagram: {e}")

    def serialize(self, workflow: UnifiedWorkflow) -> str:
        try:
            lines = ["stateDiagram-v2"]

            # Add initial states
            initial_states = [s for s in workflow.states.values() if s.is_initial]
            for state in initial_states:
                lines.append(f"    [*] --> {state.name}")

            # Add state descriptions as notes
            for state in workflow.states.values():
                if state.description:
                    lines.extend(
                        [
                            f"    note right of {state.name}",
                            f"        {state.description}",
                            "    end note",
                        ]
                    )

            # Add transitions
            for trans in workflow.transitions:
                # Combine conditions into label
                label = " && ".join(
                    f"{c.field} {c.operator} {c.value}"
                    for c in trans.conditions
                    if c.field == "condition"  # Only use condition-type conditions
                )

                if label:
                    lines.append(
                        f"    {trans.from_state} --> {trans.to_state}: {label}"
                    )
                else:
                    lines.append(f"    {trans.from_state} --> {trans.to_state}")

            # Add terminal states
            terminal_states = [s for s in workflow.states.values() if s.is_terminal]
            for state in terminal_states:
                lines.append(f"    {state.name} --> [*]")

            return "\n".join(lines)

        except Exception as e:
            raise ParserError(f"Error serializing to Mermaid format: {e}")
