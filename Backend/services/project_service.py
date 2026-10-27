from sqlalchemy.orm import Session
from respos.project import ProjectRepo
from schemas.project import ProjectCreate

from services.code_chunk_service import ChunkCodeService
from services.github_injestion_service import GitHubInjestionService
from services.embedding_pipeline import EmbeddingPipeline

class ProjectService:

    def __init__(self, db:Session):
        self.db = db
        self.repository = ProjectRepo(db)
        self.chunk_code = ChunkCodeService(db)
        self.ingestionService = GitHubInjestionService()
        self.embedding_chunks = EmbeddingPipeline(db)

    async def create_project(self, project_data: ProjectCreate, user_id: int):
        project = self.repository.create(project_data, user_id)

        if not project.repository_url:
            return project

        ingestion_res = await self.ingestionService.injest_repo(
            project.repository_url
        )

        self.chunk_code.process_and_store(
            project_id = project.id,
            files = ingestion_res['files']
        )

        embedding_res = self.embedding_chunks.index_project(
            project_id = project.id
        )

        print(embedding_res)

        return project

    def get_project(self, user_id : int):
        return self.repository.get_all(user_id)

    def get_projects_by_id(self, project_id:int, user_id: int):
        return self.repository.get_by_id(project_id, user_id)