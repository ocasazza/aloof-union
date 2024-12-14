from typing import Dict, Union

from ..exceptions import ParserError, TranspilerError, ValidationError
from .models import AutomationType, UnifiedWorkflow
from .parsers import FreshServiceParser, JSMParser, MermaidParser, WorkflowParser


class WorkflowTranspiler:
    def __init__(self):
        self._parsers: Dict[AutomationType, WorkflowParser] = {
            AutomationType.FRESHSERVICE: FreshServiceParser(),
            AutomationType.JSM: JSMParser(),
            AutomationType.MERMAID: MermaidParser(),
        }

    def validate_workflow(self, workflow: UnifiedWorkflow) -> None:
        """
        Validates the unified workflow format.

        Args:
            workflow: The workflow to validate

        Raises:
            ValidationError: If the workflow is invalid
        """
        # Check for at least one state
        if not workflow.states:
            raise ValidationError("Workflow must have at least one state")

        # Check for initial state
        initial_states = [s for s in workflow.states.values() if s.is_initial]
        if not initial_states:
            raise ValidationError("Workflow must have an initial state")

        # Validate transitions
        for transition in workflow.transitions:
            if transition.from_state not in workflow.states:
                raise ValidationError(
                    f"Invalid from_state in transition: {transition.from_state}"
                )
            if transition.to_state not in workflow.states:
                raise ValidationError(
                    f"Invalid to_state in transition: {transition.to_state}"
                )

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
            content: The input workflow content
            from_type: The source format type
            to_type: The target format type
            validate: Whether to validate the workflow during conversion

        Returns:
            The workflow in the target format

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
                self.validate_workflow(unified)

            # Convert to target format
            return target_parser.serialize(unified)

        except KeyError as e:
            raise TranspilerError(f"Unsupported format type: {e}")
        except (ValidationError, ParserError) as e:
            raise
        except Exception as e:
            raise TranspilerError(f"Error during transpilation: {e}")
