from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

from trl import SFTConfig, SFTTrainer
from peft import LoraConfig
import pandas as pd
from datasets import Dataset
import pandas as pd
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig, setup_chat_format
import torch


data = pd.read_json("formatted_player_analysis_data.jsonl", lines=True)  # Replace with your file path
dataset = Dataset.from_pandas(data)


model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
# Load the model and tokenizer with device settings for GPU
model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",         # Automatically maps model to available GPUs
    torch_dtype=torch.float16   # Use half-precision for faster training
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set up the chat format
model, tokenizer = setup_chat_format(model, tokenizer)


def formatting_func(example):
    return [f"### Prompt: {example['prompt']}\n### Completion: {example['completion']}"]

# Configure the SFT trainer with GPU support
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=SFTConfig(
        output_dir="/tmp",
        logging_dir="/tmp/logs",  # Directory for logs
        #save_steps=1000,  
        # Set save intervals for the adapter weights
        save_strategy="no",
        evaluation_strategy="no",
        # evaluation_strategy="no",
        num_train_epochs=200,
        fp16=True,
        per_device_train_batch_size=1# Enable half-precision training (float16)
    ),
    peft_config=peft_config,
    formatting_func=formatting_func,
    processing_class=tokenizer
)

# Train the model
trainer.train()


trainer.model.save_pretrained("tmp/adapter_weights")