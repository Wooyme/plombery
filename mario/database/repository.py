from typing import List
from datetime import datetime

from mario.pipeline.pipeline import PipelineRunStatus

from .base import SessionLocal
from .schemas import PipelineRunCreate
from . import models


def create_pipeline_run(data: PipelineRunCreate):
    db = SessionLocal()
    db.expire_on_commit = False

    created_model = models.PipelineRun(**data.dict())
    db.add(created_model)
    db.commit()
    db.refresh(created_model)
    return created_model


def update_pipeline_run(
    pipeline_run: models.PipelineRun, end_time: datetime, status: PipelineRunStatus
):
    db = SessionLocal()

    pipeline_run.duration = (end_time - pipeline_run.start_time).total_seconds() * 1000
    pipeline_run.status = status.value

    db.query(models.PipelineRun).filter(
        models.PipelineRun.id == pipeline_run.id
    ).update(
        dict(
            duration=pipeline_run.duration,
            status=pipeline_run.status,
        )
    )

    db.commit()


def list_pipeline_runs(pipeline_id: str, trigger_id: str):
    db = SessionLocal()
    db.expire_on_commit = False

    pipeline_runs: List[models.PipelineRun] = (
        db.query(models.PipelineRun)
        .filter(
            models.PipelineRun.pipeline_id == pipeline_id,
            models.PipelineRun.trigger_id == trigger_id,
        )
        .order_by(models.PipelineRun.id.desc())
        .limit(30)
        .all()
    )

    return pipeline_runs


def get_pipeline_run(pipeline_run_id: int):
    db = SessionLocal()

    pipeline_run: models.PipelineRun = db.query(models.PipelineRun).get(pipeline_run_id)

    return pipeline_run


def get_latest_pipeline_run(pipeline_id, trigger_id):
    db = SessionLocal()

    pipeline_run: models.PipelineRun = (
        db.query(models.PipelineRun)
        .filter(
            models.PipelineRun.pipeline_id == pipeline_id,
            models.PipelineRun.trigger_id == trigger_id,
        )
        .order_by(models.PipelineRun.id.desc())
        .first()
    )

    return pipeline_run
