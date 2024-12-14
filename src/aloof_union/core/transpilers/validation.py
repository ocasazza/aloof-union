# aloof_union/transpilers/validation.py
from typing import Set

from aloof_union.core.models import UnifiedWorkflow
from aloof_union.exceptions import ValidationError


class WorkflowValidator:
    """Handles workflow validation rules and checks."""

    @staticmethod
    def validate_states(workflow: UnifiedWorkflow) -> None:
        """Validate workflow states."""
        if not workflow.states:
            raise ValidationError("Workflow must have at least one state")

        # Check for initial state
        initial_states = [s for s in workflow.states.values() if s.is_initial]
        if not initial_states:
            raise ValidationError("Workflow must have an initial state")
        if len(initial_states) > 1:
            raise ValidationError("Workflow cannot have multiple initial states")

    @staticmethod
    def validate_transitions(workflow: UnifiedWorkflow) -> None:
        """Validate workflow transitions."""
        state_names = set(workflow.states.keys())

        for transition in workflow.transitions:
            # Check for valid state references
            if transition.from_state not in state_names:
                raise ValidationError(
                    f"Invalid from_state in transition: {transition.from_state}"
                )
            if transition.to_state not in state_names:
                raise ValidationError(
                    f"Invalid to_state in transition: {transition.to_state}"
                )

    @staticmethod
    def validate_reachability(workflow: UnifiedWorkflow) -> None:
        """Validate that all states are reachable."""
        initial_states = [s.name for s in workflow.states.values() if s.is_initial]
        if not initial_states:
            return  # Already checked in validate_states

        # Build adjacency list
        adjacency: Dict[str, Set[str]] = {state: set() for state in workflow.states}
        for trans in workflow.transitions:
            adjacency[trans.from_state].add(trans.to_state)

        # Perform DFS from initial state
        visited = set()

        def dfs(state: str) -> None:
            visited.add(state)
            for next_state in adjacency[state]:
                if next_state not in visited:
                    dfs(next_state)

        dfs(initial_states[0])

        # Check for unreachable states
        unreachable = set(workflow.states.keys()) - visited
        if unreachable:
            raise ValidationError(
                f"Following states are unreachable: {', '.join(unreachable)}"
            )

    @staticmethod
    def validate_terminal_states(workflow: UnifiedWorkflow) -> None:
        """Validate terminal states configuration."""
        terminal_states = set(s.name for s in workflow.states.values() if s.is_terminal)

        # Check that terminal states have no outgoing transitions
        for trans in workflow.transitions:
            if trans.from_state in terminal_states:
                raise ValidationError(
                    f"Terminal state {trans.from_state} cannot have outgoing transitions"
                )

    @staticmethod
    def validate_conditions(workflow: UnifiedWorkflow) -> None:
        """Validate transition conditions."""
        for trans in workflow.transitions:
            # Check for conflicting conditions
            field_operators = set()
            for condition in trans.conditions:
                field_op = (condition.field, condition.operator)
                if field_op in field_operators:
                    raise ValidationError(
                        f"Conflicting conditions for {condition.field} "
                        f"in transition {trans.from_state} -> {trans.to_state}"
                    )
                field_operators.add(field_op)

    def validate_workflow(self, workflow: UnifiedWorkflow) -> None:
        """
        Run all validation checks on a workflow.

        Args:
            workflow: The workflow to validate

        Raises:
            ValidationError: If any validation check fails
        """
        self.validate_states(workflow)
        self.validate_transitions(workflow)
        self.validate_reachability(workflow)
        self.validate_terminal_states(workflow)
        self.validate_conditions(workflow)
