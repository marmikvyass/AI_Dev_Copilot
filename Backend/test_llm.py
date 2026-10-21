from rag.llm_generation import LLM_Generate

def main():
    llm = LLM_Generate()
    answer = llm.generate("Explain what python function is in two sentence")
    print(answer)

if __name__ == '__main__':
    main()