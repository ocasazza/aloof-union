# aloof_union/transpilers/workflow.py
from typing import Dict, Union

from aloof_union.core.models import AutomationType, UnifiedWorkflow
from aloof_union.exceptions import TranspilerError

from ..parsers import FreshServiceParser, JSMParser, MermaidParser, WorkflowParser
from .base import BaseTranspiler
from .validation import WorkflowValidator


class WorkflowTranspiler(BaseTranspiler):
    """
    Main transpiler class for converting between workflow formats.
    """

    def __init__(self):
        self._validator = WorkflowValidator()
        self._parsers: Dict[AutomationType, WorkflowParser] = {
            AutomationType.FRESHSERVICE: FreshServiceParser(),
            AutomationType.JSM: JSMParser(),
            AutomationType.MERMAID: MermaidParser(),
        }

    def validate(self, workflow: UnifiedWorkflow) -> None:
        """
        Validate a workflow using the workflow validator.

        Args:
            workflow: The workflow to validate

        Raises:
            ValidationError: If validation fails
        """
        self._validator.validate_workflow(workflow)

    def transpile(
        self,
        content: Union[str, dict],
        from_type: AutomationType,
        to_type: AutomationType,
        validate: bool = True,
    ) -> Union[str, dict]:
        """
        Transpile from one workflow format to another.

        Args:
            content: The workflow content to transpile
            from_type: The source format type
            to_type: The target format type
            validate: Whether to validate during transpilation

        Returns:
            The transpiled workflow content

        Raises:
            TranspilerError: If transpilation fails
            ValidationError: If workflow validation fails
        """
        try:
            # Get appropriate parsers
            source_parser = self._parsers[from_type]
            target_parser = self._parsers[to_type]

            # Parse to unified format
            unified = source_parser.parse(content)

            # Validate if requested
            if validate:
                self.validate(unified)

            # Convert to target format
            return target_parser.serialize(unified)

        except KeyError as e:
            raise TranspilerError(f"Unsupported format type: {e}")
        except Exception as e:
            raise TranspilerError(f"Error during transpilation: {e}")
