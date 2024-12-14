# aloof_union/parsers/base.py
from abc import ABC, abstractmethod
from typing import Union

from aloof_union.core.models import UnifiedWorkflow


class WorkflowParser(ABC):
    @abstractmethod
    def parse(self, content: Union[str, dict]) -> UnifiedWorkflow:
        """Parse content into unified workflow format."""
        pass

    @abstractmethod
    def serialize(self, workflow: UnifiedWorkflow) -> Union[str, dict]:
        """Serialize unified workflow to target format."""
        pass
