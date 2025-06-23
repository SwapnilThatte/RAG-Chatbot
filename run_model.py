from langchain_ollama import ChatOllama


SYSTEM_PROMPT = """You are helpful AI assistant. You answer questions truthfully. 
        If you do not know answer to a perticular question then you say so.
        You do not promote any bad language, illegal activities and have no personal views on politics.
        If you are asked any questions about personal opinions on sensetive topics then you politely refuse to state any opnions."""


# USE THIS CODE IF USING OLLAMA
llm = ChatOllama(
    model="mistral",
    temperature=0,
    num_predict=512,
    num_ctx=1024,
    tfs_z=1.8,
)

def generate_response(prompt: str, context: str = "", history: list = []) -> str:

    BASE_MESSAGE = [{"role" : "system", "content" : SYSTEM_PROMPT}] + history

    if context == "":
        message = BASE_MESSAGE + [{"role" : "user", "content" : prompt}]
    else:
        message = BASE_MESSAGE + [{"role" : "user", "content" : f"Context : {context}\nQuery : {prompt}"}]


    # Generate response
    response = llm.invoke(message)
    return response.content

