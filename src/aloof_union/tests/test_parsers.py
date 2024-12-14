# aloof_union/tests/test_parsers.py
import pytest

from aloof_union.core.parsers import FreshServiceParser, JSMParser, MermaidParser
from aloof_union.exceptions import ParserError


class TestFreshServiceParser:
    def test_parse_simple_workflow(self, simple_fs_workflow):
        parser = FreshServiceParser()
        workflow = parser.parse(simple_fs_workflow)

        assert len(workflow.states) == 3
        assert workflow.states["New"].is_initial
        assert workflow.states["Resolved"].is_terminal
        assert len(workflow.transitions) == 2

        # Verify transition details
        first_transition = workflow.transitions[0]
        assert first_transition.from_state == "New"
        assert first_transition.to_state == "In Progress"
        assert len(first_transition.conditions) == 1
        assert first_transition.conditions[0].field == "assignee"

    def test_parse_complex_workflow(self, complex_fs_workflow):
        parser = FreshServiceParser()
        workflow = parser.parse(complex_fs_workflow)

        assert len(workflow.states) == 6
        assert len(workflow.transitions) == 7
        assert workflow.states["New"].is_initial
        assert workflow.states["Closed"].is_terminal

    def test_serialize_workflow(self, unified_workflow):
        parser = FreshServiceParser()
        result = parser.serialize(unified_workflow)

        assert "states" in result
        assert "transitions" in result
        assert len(result["states"]) == len(unified_workflow.states)
        assert len(result["transitions"]) == len(unified_workflow.transitions)


class TestJSMParser:
    def test_parse_simple_workflow(self, simple_jsm_workflow):
        parser = JSMParser()
        workflow = parser.parse(simple_jsm_workflow)

        assert len(workflow.states) == 3
        assert workflow.states["Open"].is_initial
        assert workflow.states["Done"].is_terminal
        assert len(workflow.transitions) == 2

    def test_status_categories(self, simple_jsm_workflow):
        parser = JSMParser()
        workflow = parser.parse(simple_jsm_workflow)

        assert workflow.states["Open"].properties["statusCategory"] == "NEW"
        assert (
            workflow.states["In Progress"].properties["statusCategory"] == "IN_PROGRESS"
        )
        assert workflow.states["Done"].properties["statusCategory"] == "DONE"

    def test_serialize_workflow(self, unified_workflow):
        parser = JSMParser()
        result = parser.serialize(unified_workflow)

        assert "statuses" in result
        assert "rules" in result
        assert len(result["statuses"]) == len(unified_workflow.states)
        assert len(result["rules"]) == len(unified_workflow.transitions)


class TestMermaidParser:
    def test_parse_simple_workflow(self, simple_mermaid_workflow):
        parser = MermaidParser()
        workflow = parser.parse(simple_mermaid_workflow)

        assert len(workflow.states) == 3
        assert len(workflow.transitions) == 3  # Including terminal transition

        # Verify state descriptions from notes
        assert "newly created" in workflow.states["New"].description.lower()

    def test_parse_complex_workflow(self, complex_mermaid_workflow):
        parser = MermaidParser()
        workflow = parser.parse(complex_mermaid_workflow)

        assert len(workflow.states) == 7  # Including start/end states
        assert len(workflow.transitions) > 5

        # Verify complex conditions
        progress_transition = next(
            t
            for t in workflow.transitions
            if t.from_state == "New" and t.to_state == "InProgress"
        )
        assert len(progress_transition.conditions) == 2

    def test_serialize_workflow(self, unified_workflow):
        parser = MermaidParser()
        result = parser.serialize(unified_workflow)

        assert "stateDiagram-v2" in result
        assert "[*] -->" in result  # Initial state transition
        assert "-->" in result  # Regular transitions
        assert "note right of" in result  # State descriptions
