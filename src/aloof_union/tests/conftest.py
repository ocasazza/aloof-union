# aloof_union/tests/conftest.py
import pytest

from aloof_union.core.models import (
    Action,
    Condition,
    Transition,
    UnifiedWorkflow,
    WorkflowState,
)


@pytest.fixture
def simple_fs_workflow():
    """Simple Fresh Service workflow fixture."""
    return {
        "states": {
            "New": {"is_initial": True, "description": "Ticket newly created"},
            "In Progress": {"description": "Agent working on ticket"},
            "Resolved": {"description": "Solution provided", "is_terminal": True},
        },
        "transitions": [
            {
                "from_state": "New",
                "to_state": "In Progress",
                "conditions": [
                    {"field": "assignee", "operator": "is not", "value": None}
                ],
                "actions": [
                    {"type": "notify", "parameters": {"template": "ticket_assigned"}}
                ],
            },
            {
                "from_state": "In Progress",
                "to_state": "Resolved",
                "conditions": [
                    {"field": "resolution", "operator": "is not", "value": None}
                ],
                "actions": [
                    {"type": "notify", "parameters": {"template": "ticket_resolved"}}
                ],
            },
        ],
    }


@pytest.fixture
def complex_fs_workflow():
    """Complex Fresh Service workflow with multiple paths and conditions."""
    return {
        "states": {
            "New": {"is_initial": True, "description": "Initial ticket state"},
            "Pending": {"description": "Awaiting more information"},
            "In Progress": {"description": "Being worked on"},
            "Under Review": {"description": "Solution being reviewed"},
            "Resolved": {"description": "Solution implemented"},
            "Closed": {"description": "Ticket completed", "is_terminal": True},
        },
        "transitions": [
            {
                "from_state": "New",
                "to_state": "Pending",
                "conditions": [
                    {"field": "info_required", "operator": "equals", "value": True}
                ],
                "actions": [
                    {"type": "notify", "parameters": {"template": "info_needed"}}
                ],
            },
            {
                "from_state": "New",
                "to_state": "In Progress",
                "conditions": [
                    {"field": "assignee", "operator": "is not", "value": None},
                    {"field": "priority", "operator": "exists", "value": True},
                ],
                "actions": [
                    {"type": "notify", "parameters": {"template": "work_started"}}
                ],
            },
            {
                "from_state": "Pending",
                "to_state": "In Progress",
                "conditions": [
                    {"field": "customer_response", "operator": "exists", "value": True}
                ],
            },
            {
                "from_state": "In Progress",
                "to_state": "Under Review",
                "conditions": [
                    {"field": "solution", "operator": "exists", "value": True}
                ],
            },
            {
                "from_state": "Under Review",
                "to_state": "Resolved",
                "conditions": [
                    {"field": "review_passed", "operator": "equals", "value": True}
                ],
            },
            {
                "from_state": "Under Review",
                "to_state": "In Progress",
                "conditions": [
                    {"field": "review_passed", "operator": "equals", "value": False}
                ],
            },
            {
                "from_state": "Resolved",
                "to_state": "Closed",
                "conditions": [
                    {"field": "customer_satisfied", "operator": "equals", "value": True}
                ],
            },
        ],
    }


@pytest.fixture
def simple_jsm_workflow():
    """Simple JSM workflow fixture."""
    return {
        "statuses": [
            {
                "name": "Open",
                "description": "New issue reported",
                "initial": True,
                "statusCategory": "NEW",
            },
            {
                "name": "In Progress",
                "description": "Issue being investigated",
                "statusCategory": "IN_PROGRESS",
            },
            {"name": "Done", "description": "Issue resolved", "statusCategory": "DONE"},
        ],
        "rules": [
            {
                "fromStatus": "Open",
                "toStatus": "In Progress",
                "conditions": [
                    {"field": {"name": "assignee"}, "operator": "is not empty"}
                ],
                "postFunctions": [
                    {
                        "type": "FireIssueEventFunction",
                        "configuration": {"eventType": "issue_assigned"},
                    }
                ],
            },
            {
                "fromStatus": "In Progress",
                "toStatus": "Done",
                "conditions": [
                    {"field": {"name": "resolution"}, "operator": "is not empty"}
                ],
                "postFunctions": [
                    {
                        "type": "FireIssueEventFunction",
                        "configuration": {"eventType": "issue_resolved"},
                    }
                ],
            },
        ],
    }


@pytest.fixture
def simple_mermaid_workflow():
    """Simple Mermaid workflow fixture."""
    return """
stateDiagram-v2
    [*] --> New
    New --> InProgress: assignee set
    InProgress --> Resolved: resolution provided
    Resolved --> [*]
    
    note right of New
        Ticket newly created
    end note
    
    note right of InProgress
        Agent working on ticket
    end note
    
    note right of Resolved
        Solution provided
    end note
"""


@pytest.fixture
def complex_mermaid_workflow():
    """Complex Mermaid workflow with multiple paths and conditions."""
    return """
stateDiagram-v2
    [*] --> New
    New --> Pending: needs_info
    New --> InProgress: assigned && prioritized
    Pending --> InProgress: info_received
    InProgress --> UnderReview: solution_proposed
    UnderReview --> Resolved: review_approved
    UnderReview --> InProgress: review_failed
    Resolved --> Closed: customer_accepted
    Closed --> [*]
    
    note right of New
        Initial ticket state
    end note
    
    note right of Pending
        Awaiting more information
    end note
    
    note right of InProgress
        Being worked on
    end note
    
    note right of UnderReview
        Solution being reviewed
    end note
    
    note right of Resolved
        Solution implemented
    end note
    
    note right of Closed
        Ticket completed
    end note
"""


@pytest.fixture
def invalid_workflow_no_initial():
    """Invalid workflow with no initial state."""
    return {
        "states": {
            "Open": {"description": "Ticket open"},
            "Closed": {"description": "Ticket closed", "is_terminal": True},
        },
        "transitions": [
            {
                "from_state": "Open",
                "to_state": "Closed",
                "conditions": [],
                "actions": [],
            }
        ],
    }


@pytest.fixture
def invalid_workflow_unreachable():
    """Invalid workflow with unreachable states."""
    return {
        "states": {
            "New": {"is_initial": True, "description": "New ticket"},
            "In Progress": {"description": "Being worked on"},
            "Resolved": {"description": "Resolved ticket", "is_terminal": True},
            "Abandoned": {"description": "Unreachable state"},
        },
        "transitions": [
            {
                "from_state": "New",
                "to_state": "In Progress",
                "conditions": [],
                "actions": [],
            },
            {
                "from_state": "In Progress",
                "to_state": "Resolved",
                "conditions": [],
                "actions": [],
            },
        ],
    }


@pytest.fixture
def invalid_workflow_terminal_transition():
    """Invalid workflow with transition from terminal state."""
    return {
        "states": {
            "New": {"is_initial": True, "description": "New ticket"},
            "Closed": {"description": "Closed ticket", "is_terminal": True},
            "Reopened": {"description": "Reopened ticket"},
        },
        "transitions": [
            {
                "from_state": "New",
                "to_state": "Closed",
                "conditions": [],
                "actions": [],
            },
            {
                "from_state": "Closed",
                "to_state": "Reopened",
                "conditions": [],
                "actions": [],
            },
        ],
    }


@pytest.fixture
def unified_workflow():
    """Unified workflow representation fixture."""
    states = {
        "New": WorkflowState(name="New", description="New ticket", is_initial=True),
        "In Progress": WorkflowState(name="In Progress", description="Being worked on"),
        "Resolved": WorkflowState(
            name="Resolved", description="Ticket resolved", is_terminal=True
        ),
    }

    transitions = [
        Transition(
            from_state="New",
            to_state="In Progress",
            conditions=[Condition("assignee", "is not", None)],
            actions=[Action("notify", {"template": "assigned"})],
        ),
        Transition(
            from_state="In Progress",
            to_state="Resolved",
            conditions=[Condition("resolution", "exists", True)],
            actions=[Action("notify", {"template": "resolved"})],
        ),
    ]

    return UnifiedWorkflow(
        states=states, transitions=transitions, metadata={"source": "test"}
    )
