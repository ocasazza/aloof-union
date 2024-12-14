from pathlib import Path
from typing import Any, Dict

import pytest


# Test utilities
def get_test_data_path() -> Path:
    """Returns the path to the test data directory."""
    return Path(__file__).parent / "data"


def load_test_workflow(filename: str) -> Dict[str, Any]:
    """Helper to load a workflow from the test data directory."""
    path = get_test_data_path() / filename
    if not path.exists():
        raise FileNotFoundError(f"Test workflow file not found: {filename}")
    return path.read_text()


# Common test constants
TEST_WORKFLOWS = {
    "simple_fs": "simple_freshservice.json",
    "complex_fs": "complex_freshservice.json",
    "simple_jsm": "simple_jsm.json",
    "complex_jsm": "complex_jsm.json",
    "simple_mermaid": "simple_mermaid.txt",
    "complex_mermaid": "complex_mermaid.txt",
}

# Test markers
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.parser = pytest.mark.parser
pytest.mark.transpiler = pytest.mark.transpiler
pytest.mark.validation = pytest.mark.validation

# Test categories for better organization
pytest.mark.freshservice = pytest.mark.freshservice
pytest.mark.jsm = pytest.mark.jsm
pytest.mark.mermaid = pytest.mark.mermaid

# Optional performance testing
pytest.mark.slow = pytest.mark.slow
