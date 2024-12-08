# from flask import Flask, request, jsonify
# from flask_cors import CORS
import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments,BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, PeftModel, prepare_model_for_kbit_training


# app = Flask(__name__)
# CORS(app) 

model_name = "meta-llama/Llama-3.1-8B"
output_dir = "/home/uav/Documents/AI_Hunter/AI_Capstone_old/test1"
base_model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
lora_model = PeftModel.from_pretrained(base_model, output_dir)
lora_model.eval()

# Now run inference
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


def chat(user_query):
    prompt = f"""You're a professional scout and you have complete knowledge on Football and now we are just scouting for players with in this league(MLS)
    so main things to consider when you suggest player
    1)Salary/Contract Terms:
    2)Positional Fit and Statistical Performance
    3)Adaptability to Playing Style
    4)Physical and Technical Attributes
    5)Personality, Professionalism, and Team Chemistry
    Query:{user_query}"""
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = lora_model.generate(**inputs, max_length=1536)#,do_sample=False,temperature=0.0)
    # return tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    try:
        response.split("Response:")[1]
        if len(response) > 1:
            return response.split("Response:")[1]
    except:
        return response



# @app.route("/chat", methods=["POST"])
# def handle_chat():
#     try:
#         data = request.json
#         user_query = data.get("query", "")

#         if not user_query:
#             return jsonify({"error": "Query not provided"}), 400

#         response = chat(user_query)
#         return jsonify({"response": response})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

# Define Gradio interface
def player_scouting_interface(user_query):
    return chat(user_query)

interface = gr.Interface(
    fn=player_scouting_interface,
    inputs=gr.Textbox(label="Enter Your Query", placeholder="Type your question about scouting players..."),
    outputs=gr.Textbox(label="Chat Output"),
    title="Player Scouting",
    description="Enter your query about scouting players, and get insights from the model."
)

# Launch Gradio app
if __name__ == "__main__":
    interface.launch(share=True)