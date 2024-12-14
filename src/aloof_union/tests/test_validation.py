# aloof_union/tests/test_validation.py
import pytest

from aloof_union.core.transpilers.validation import WorkflowValidator
from aloof_union.exceptions import ValidationError


class TestWorkflowValidator:
    def test_validate_valid_workflow(self, unified_workflow):
        validator = WorkflowValidator()
        # Should not raise any exceptions
        validator.validate_workflow(unified_workflow)

    def test_validate_no_initial_state(self, invalid_workflow_no_initial):
        validator = WorkflowValidator()
        with pytest.raises(ValidationError, match="must have an initial state"):
            validator.validate_workflow(invalid_workflow_no_initial)

    def test_validate_unreachable_states(self, invalid_workflow_unreachable):
        validator = WorkflowValidator()
        with pytest.raises(ValidationError, match="states are unreachable"):
            validator.validate_workflow(invalid_workflow_unreachable)

    def test_validate_terminal_state_transition(
        self, invalid_workflow_terminal_transition
    ):
        validator = WorkflowValidator()
        with pytest.raises(ValidationError, match="cannot have outgoing transitions"):
            validator.validate_workflow(invalid_workflow_terminal_transition)
