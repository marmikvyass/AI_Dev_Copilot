from core.dbconnect import Session
from models.code_chunk import CodeChunk

db = Session()

project_id = 13  # Replace with the newly created project ID

chunks = (
    db.query(CodeChunk)
    .filter(CodeChunk.project_id == project_id)
    .all()
)

print("Total chunks:", len(chunks))

for chunk in chunks[:5]:
    print(chunk.file_path, chunk.chunk_index)

db.close()