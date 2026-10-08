
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.users import Users
from core.dbconnect import get_db
from schemas.project import ProjectResponse, ProjectCreate
from services.project_service import ProjectService
from core.dependencies import get_current_user
router = APIRouter(
    prefix='/project',
    tags=['Project']
)

@router.post('/', response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db), current_user : Users = Depends(get_current_user)):
    service = ProjectService(db)

    return service.create_project(project_data, current_user.id)

@router.get('/', response_model=list[ProjectResponse])
def list_project(db: Session = Depends(get_db), current_user : Users = Depends(get_current_user)):
    service = ProjectService(db)

    return service.get_project(current_user.id)

@router.get('/{project_id}', response_model=ProjectResponse)
def get_project_by_id(project_id: int, db :Session = Depends(get_db), current_user : Users = Depends(get_current_user) ):
    service = ProjectService(db)
    project = service.get_projects_by_id(project_id, current_user.id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail='Project not found'
        )

    return project



