from pydantic import BaseModel, Field


class AskQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

class ResourceRes(BaseModel):
    file_path : str
    chunk_index: int
    distance: float
class AskQuesResponse(BaseModel):
    project_id: int
    question: str
    answer: str
    sources: list[ResourceRes]

