from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"

class TriggerMessage(BaseModel):
    trigger_id: str = Field(..., description="Trigger message ID")
    trigger_type: str = Field(..., description="Trigger message type")
    message: str = Field(..., description="Trigger message content")
    received_time: datetime = Field(default_factory=datetime.now, description="Trigger message received time")

class ProductionTask(BaseModel):
    kafka_id: str = Field(..., description="Kafka message ID")
    task_name: str = Field(..., description="Production task name")
    start_time: datetime = Field(default_factory=datetime.now, description="Production task start time")
    end_time: datetime = Field(None, description="Production task end time")
    status: TaskStatusEnum = Field(TaskStatusEnum.PENDING, description="Production task status")
    airflow_run_id: str = Field(None, description="Airflow run ID")

class Result(BaseModel):
    task_id: str = Field(..., description="Production task ID")
    result: str = Field(..., description="Result")
    storage_path: str = Field(..., description="Result storage path")
