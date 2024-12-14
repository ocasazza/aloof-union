# aloof_union/tests/test_transpiler.py
import pytest

from aloof_union.core.models import AutomationType
from aloof_union.core.transpilers import WorkflowTranspiler
from aloof_union.exceptions import TranspilerError, ValidationError


class TestWorkflowTranspiler:
    def test_fs_to_mermaid(self, simple_fs_workflow):
        transpiler = WorkflowTranspiler()
        result = transpiler.transpile(
            simple_fs_workflow, AutomationType.FRESHSERVICE, AutomationType.MERMAID
        )

        assert "stateDiagram-v2" in result
        assert "New" in result
        assert "In Progress" in result
        assert "Resolved" in result
        assert "[*] -->" in result  # Initial state

    def test_mermaid_to_fs(self, simple_mermaid_workflow):
        transpiler = WorkflowTranspiler()
        result = transpiler.transpile(
            simple_mermaid_workflow, AutomationType.MERMAID, AutomationType.FRESHSERVICE
        )

        assert "states" in result
        assert "transitions" in result
        assert "New" in result["states"]

    def test_jsm_to_fs(self, simple_jsm_workflow):
        transpiler = WorkflowTranspiler()
        result = transpiler.transpile(
            simple_jsm_workflow, AutomationType.JSM, AutomationType.FRESHSERVICE
        )

        assert "states" in result
        assert "transitions" in result
        assert len(result["states"]) == 3

    def test_invalid_format(self, simple_fs_workflow):
        transpiler = WorkflowTranspiler()
        with pytest.raises(TranspilerError, match="Unsupported format"):
            transpiler.transpile(
                simple_fs_workflow, "invalid_format", AutomationType.MERMAID
            )

    def test_validation_during_transpile(self, invalid_workflow_no_initial):
        transpiler = WorkflowTranspiler()
        with pytest.raises(ValidationError):
            transpiler.transpile(
                invalid_workflow_no_initial,
                AutomationType.FRESHSERVICE,
                AutomationType.MERMAID,
            )

    def test_transpile_without_validation(self, invalid_workflow_no_initial):
        transpiler = WorkflowTranspiler()
        # Should not raise validation error when validate=False
        result = transpiler.transpile(
            invalid_workflow_no_initial,
            AutomationType.FRESHSERVICE,
            AutomationType.MERMAID,
            validate=False,
        )
        assert result is not None
