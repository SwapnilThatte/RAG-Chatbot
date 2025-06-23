# from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
# from huggingface_hub import hf_hub_download
# import os
# from transformers import pipeline
# import torch
from llama_cpp import Llama




# MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"

# quantization_config = BitsAndBytesConfig(load_in_4bit=True)

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME, 
#     device_map="auto", 
#     torch_dtype=torch.float16,
# )
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# print(f"Microsoft Phi-3.5-mini-instruct Downloaded Successfully !")


# generation_args = {
#     "max_new_tokens": 64,
#     "return_full_text": False,
#     "temperature": 0.1,
#     "top_p": 1.0,
#     "do_sample": True,
# }

# model.eval()

# pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=64, 
#     temperature=0.4, 
#     do_sample=True
# )

def generate_response(prompt: str, context: str = "", history: list = []) -> str:


    # phi-2.Q4_K_S.gguf
    llm = Llama.from_pretrained(
        repo_id="TheBloke/phi-2-GGUF",
        filename="*Q4_K_S.gguf",
        verbose=False,
        n_gpu_layers=0,
        n_ctx=512
    )
    
    # BASE_MESSAGE = [{"role" : "system", "content" : SYSTEM_PROMPT}] + history

    # if context == "":
    #     message = BASE_MESSAGE + [{"role" : "user", "content" : prompt}]
    # else:
    #     message = BASE_MESSAGE + [{"role" : "user", "content" : f"Context : {context}\nQuery : {prompt}"}]

    if context != "":
        message = f"{prompt}  Context : {context}"
    else:
        message = prompt

    responses = llm("Q: {message}  A : ",max_tokens=64, echo=False)
    # reply = responses["choices"][0]["message"]["content"]
    print(responses)
    reply = responses["choices"][0]["text"]

    # outputs = pipe(message, **generation_args)
    # outputs = pipe(message)
    # with torch.no_grad():
    #     prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in message])
    #     inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
    #     outputs = model.generate(**inputs, temperature=0.1, do_sample=True, max_new_tokens=64) 
    #     outputs = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply
    # return outputs