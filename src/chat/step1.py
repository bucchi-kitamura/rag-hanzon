from llama_index.llms.ollama import Ollama

def main():
    llm = Ollama(
        model="schroneko/gemma-2-2b-jpn-it"
    )

    response = llm.complete('富士山の標高は？')
    print(response)

if __name__ == "__main__":
    main()