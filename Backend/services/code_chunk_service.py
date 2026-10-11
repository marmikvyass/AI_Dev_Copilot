from sqlalchemy.orm import Session
from respos.code_chunk_repo import CodeChunkRepository
from rag.chunking_repo import ChunkingRepo

class ChunkCodeService:
    def __init__(self, db: Session):
        self.repo = CodeChunkRepository(db)
        self.chunk_repo = ChunkingRepo()


    def process_and_store(self, project_id: int, files: list[dict])-> dict:
        chunks = self.chunk_repo.chunk_files(files)

        if not chunks:
            return {
                "project_id" : project_id,
                "total_chunks" : 0,
                'saved_chunks' : 0
            }
        records = self.repo.create_many(
            project_id = project_id,
            chunks=chunks
        )

        return {
            "project_id" : project_id,
            "total_chunks" : len(records),
            'saved_chunks' : len(records)
        }

    def get_project_chunks(self, project_id: int) -> list:
        return self.repo.get_by_project(project_id)