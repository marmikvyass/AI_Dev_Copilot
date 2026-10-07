
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dbconnect import get_db
from schemas.project import ProjectResponse, ProjectCreate
from services.project_service import ProjectService
router = APIRouter(
    prefix='/project',
    tags=['Project']
)

@router.post('/', response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)

    return service.create_project(project_data)

@router.get('/', response_model=list[ProjectResponse])
def list_project(db: Session = Depends(get_db)):
    service = ProjectService(db)

    return service.get_project()

@router.get('/{project_id}', response_model=ProjectResponse)
def get_project_by_id(project_id: int, db :Session = Depends(get_db)):
    service = ProjectService(db)
    project = service.get_projects_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail='Project not found'
        )

    return project



