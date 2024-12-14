# aloof_union/transpilers/base.py
from abc import ABC, abstractmethod
from typing import Union

from aloof_union.core.models import UnifiedWorkflow


class BaseTranspiler(ABC):
    """Base class for all transpilers."""

    @abstractmethod
    def validate(self, workflow: UnifiedWorkflow) -> None:
        """
        Validate the workflow.

        Args:
            workflow: The workflow to validate

        Raises:
            ValidationError: If validation fails
        """
        pass

    @abstractmethod
    def transpile(
        self,
        content: Union[str, dict],
        from_type: str,
        to_type: str,
        validate: bool = True,
    ) -> Union[str, dict]:
        """
        Transpile content from one format to another.

        Args:
            content: The content to transpile
            from_type: Source format type
            to_type: Target format type
            validate: Whether to validate during transpilation

        Returns:
            Transpiled content

        Raises:
            TranspilerError: If transpilation fails
        """
        pass
