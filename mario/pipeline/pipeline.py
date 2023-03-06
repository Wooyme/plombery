from typing import List
from enum import Enum
import logging

from pydantic import BaseModel

from .task import Task
from .trigger import Trigger
from ._utils import to_snake_case


class PipelineRunStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Pipeline:
    params: BaseModel = None
    tasks: List[Task] = []
    triggers: List[Trigger] = []
    description: str = None

    def __init__(self) -> None:
        self.uuid = to_snake_case(self.__class__.__name__)
        self.logger = logging.getLogger(f"[P]{self.uuid}")
        self.description = self.__class__.__doc__
