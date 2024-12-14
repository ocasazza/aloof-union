# aloof_union/tests/test_integration.py
import pytest

from aloof_union.core.models import AutomationType
from aloof_union.core.transpilers import WorkflowTranspiler


class TestIntegration:
    def test_round_trip_fs(self, simple_fs_workflow):
        """Test Fresh Service -> Mermaid -> Fresh Service conversion."""
        transpiler = WorkflowTranspiler()

        # Convert to Mermaid
        mermaid = transpiler.transpile(
            simple_fs_workflow, AutomationType.FRESHSERVICE, AutomationType.MERMAID
        )

        # Convert back to Fresh Service
        result = transpiler.transpile(
            mermaid, AutomationType.MERMAID, AutomationType.FRESHSERVICE
        )

        # Verify core workflow structure is preserved
        assert len(result["states"]) == len(simple_fs_workflow["states"])
        assert len(result["transitions"]) == len(simple_fs_workflow["transitions"])

    def test_round_trip_jsm(self, simple_jsm_workflow):
        """Test JSM -> Fresh Service -> JSM conversion."""
        transpiler = WorkflowTranspiler()

        # Convert to Fresh Service
        fs = transpiler.transpile(
            simple_jsm_workflow, AutomationType.JSM, AutomationType.FRESHSERVICE
        )

        # Convert back to JSM
        result = transpiler.transpile(
            fs, AutomationType.FRESHSERVICE, AutomationType.JSM
        )

        # Verify core workflow structure is preserved
        assert len(result["statuses"]) == len(simple_jsm_workflow["statuses"])
        assert len(result["rules"]) == len(simple_jsm_workflow["rules"])

    def test_complex_workflow_conversion(self, complex_fs_workflow):
        """Test complex workflow conversion through all formats."""
        transpiler = WorkflowTranspiler()

        # Convert through all formats
        jsm = transpiler.transpile(
            complex_fs_workflow, AutomationType.FRESHSERVICE, AutomationType.JSM
        )

        mermaid = transpiler.transpile(jsm, AutomationType.JSM, AutomationType.MERMAID)

        result = transpiler.transpile(
            mermaid, AutomationType.MERMAID, AutomationType.FRESHSERVICE
        )

        # Verify core workflow structure is preserved
        assert len(result["states"]) == len(complex_fs_workflow["states"])
        assert len(result["transitions"]) == len(complex_fs_workflow["transitions"])
