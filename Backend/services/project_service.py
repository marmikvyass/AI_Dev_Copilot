from sqlalchemy.orm import Session
from respos.project import ProjectRepo
from schemas.project import ProjectCreate

class ProjectService:

    def __init__(self, db:Session):
        self.repository = ProjectRepo(db)

    def create_project(self, project_data: ProjectCreate):
        return self.repository.create(project_data)

    def get_project(self):
        return self.repository.get_all()

    def get_projects_by_id(self, project_id:int):
        return self.repository.get_by_id(project_id)