from sqlalchemy.orm import Session

from models.code_chunk import CodeChunk

class CodeChunkRepository:

    def __init__(self, db:Session):
        self.db = db

    def create_many(self, project_id: int, chunks: list[dict]) -> list[CodeChunk]:
        records = [
            CodeChunk(
                project_id = project_id,
                repository=chunk['repository'],
                file_path=chunk['file_path'],
                chunk_index=chunk['chunk_index'],
                content=chunk['content'],
            )
            for chunk in chunks
        ]

        self.db.add_all(records)
        self.db.commit()

        for record in records:
            self.db.refresh(record)

        return records

    def get_by_project(
            self,
            project_id: int
    ) -> list[CodeChunk]:
        return (
            self.db.query(CodeChunk)
            .filter(CodeChunk.project_id == project_id)
            .order_by(
                CodeChunk.file_path,
                CodeChunk.chunk_index
            )
            .all()
        )