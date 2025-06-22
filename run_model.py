# from ollama import chat, ChatResponse
# from langchain_ollama import ChatOllama
# from langchain.schema import SystemMessage, HumanMessage, AIMessage
# from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


SYSTEM_PROMPT = """You are helpful AI assistant. You answer questions truthfully. 
        If you do not know answer to a perticular question then you say so.
        You do not promote any bad language, illegal activities and have no personal views on politics.
        If you are asked any questions about personal opinions on sensetive topics then you politely refuse to state any opnions."""


# def generate_response(prompt: str, context:str="", history: list = [])->str:

#     BASE_MESSAGE = [{"role" : "system", "content" : SYSTEM_PROMPT}] + history

#     if context == "":
#         message = BASE_MESSAGE + [{"role" : "user", "content" : prompt}]
#     else:
#         message = BASE_MESSAGE + [{"role" : "user", "content" : f"Context : {context}\nQuery : {prompt}"}]

#     response: ChatResponse = chat(
#         model="mistral",
#         messages= message,
#         options={
#         "temperature":0, 
#         "num_predict":512, 
#         "num_ctx":1024, 
#         "tfs_z":1.8,
#         }
#     )
    
#     return response.message.content



## USE THIS CODE IF USING OLLAMA
# llm = ChatOllama(
#     model="mistral",
#     temperature=0,
#     num_predict=512,
#     num_ctx=1024,
#     tfs_z=1.8,
# )

# def generate_response(prompt: str, context: str = "", history: list = []) -> str:
#     # Convert raw dict history to LangChain messages
#     # messages = [SystemMessage(content=SYSTEM_PROMPT)]

#     # for entry in history:
#     #     role = entry["role"]
#     #     content = entry["content"]
#     #     if role == "user":
#     #         messages.append(HumanMessage(content=content))
#     #     elif role == "assistant":
#     #         messages.append(AIMessage(content=content))

#     # # Add current user message
#     # if context:
#     #     user_input = f"Context : {context}\nQuery : {prompt}"
#     # else:
#     #     user_input = prompt

#     # messages.append(HumanMessage(content=user_input))

#     BASE_MESSAGE = [{"role" : "system", "content" : SYSTEM_PROMPT}] + history

#     if context == "":
#         message = BASE_MESSAGE + [{"role" : "user", "content" : prompt}]
#     else:
#         message = BASE_MESSAGE + [{"role" : "user", "content" : f"Context : {context}\nQuery : {prompt}"}]


#     # Generate response
#     response = llm.invoke(message)
#     return response.content


MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    device_map="cpu", 
    torch_dtype="auto", 
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# print(f"Microsoft Phi-3.5-mini-instruct Downloaded Successfully !")


generation_args = {
    "max_new_tokens": 200,
    "return_full_text": False,
    "temperature": 0,
    "top_p": 0.1,
    "do_sample": True,
}

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)



def generate_response(prompt: str, context: str = "", history: list = []) -> str:
    
    BASE_MESSAGE = [{"role" : "system", "content" : SYSTEM_PROMPT}] + history

    if context == "":
        message = BASE_MESSAGE + [{"role" : "user", "content" : prompt}]
    else:
        message = BASE_MESSAGE + [{"role" : "user", "content" : f"Context : {context}\nQuery : {prompt}"}]

    outputs = pipe(message, **generation_args)
    return outputs