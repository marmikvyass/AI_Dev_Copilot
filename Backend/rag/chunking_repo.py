from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingRepo:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_split = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def chunk_file(self, file:dict) -> list[dict]:
        content = file['content']
        file_path = file['path']
        repository = file['repository']

        chunks = self.text_split.split_text(content)

        result = []

        for index, chunk in enumerate(chunks):
            result.append({
                'repository' : repository,
                'file_path' : file_path,
                'chunk_index' : index,
                'content' : chunk
            })
        return result

    def chunk_files(self, files: list[dict]) -> list[dict]:
        all_chunks = []

        for file in files:
            file_chunks = self.chunk_file(file)
            all_chunks.extend(file_chunks)

        return all_chunks