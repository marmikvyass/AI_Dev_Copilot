from sqlalchemy.orm import Session
from sqlalchemy import select

from models import project
from models.project import Project
from schemas.project import ProjectCreate

class ProjectRepo:
    def __init__(self, db:Session):
        self.db = db

    def create(self, project_data: ProjectCreate, user_id: int) -> Project:

        project = Project(
            name = project_data.name,
            description=project_data.description,
            repository_url=project_data.repository_url,
            user_id=user_id
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def get_all(self, user_id: int)-> list[Project]:
        result = self.db.execute(
            select(Project).where(
                Project.user_id == user_id
            )
        )
        return list(result.scalars().all())

    def get_by_id(self, project_id: int, user_id:int)-> Project:
        result = self.db.execute(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    