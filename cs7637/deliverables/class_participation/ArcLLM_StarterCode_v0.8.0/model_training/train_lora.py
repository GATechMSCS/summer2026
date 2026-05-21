import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
from training_data import data  # your data file

# === CONFIG ===
# Point to the unzipped model folder you downloaded (change path as needed)
MODEL_ID = "./phi4"           # ← Example: folder containing config.json, *.safetensors, tokenizer, etc.
OUTPUT_DIR = "./my_lora"      # ← Example: you can name this directory anything you want

NUM_EPOCHS = 3
BATCH_SIZE = 1
GRAD_ACCUM = 8 if torch.cuda.is_available() else 4

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

# Prepare dataset
dataset = Dataset.from_list(data * 5)  # The number of times to repeat the data you put in the training_data.py file.

def tokenize_fn(examples):
    tokenized = tokenizer(examples["text"], truncation=True, max_length=512, padding="max_length")
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_fn, batched=True)

# === LOAD MODEL ===
if torch.cuda.is_available():
    # GPU: 8-bit quantization (fast & memory efficient)
    quant_config = BitsAndBytesConfig(load_in_8bit=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=quant_config,
        device_map="auto",
        trust_remote_code=True
    )
else:
    # CPU: fp16 (slower but works)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="cpu",
        trust_remote_code=True
    )

model = prepare_model_for_kbit_training(model)

# === LoRA CONFIG ===
lora_config = LoraConfig(
    r=16,                      # 8–32 good balance
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # common model layers: you might find others
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# === TRAINING ===
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    num_train_epochs=NUM_EPOCHS,
    learning_rate=1e-4,
    fp16=torch.cuda.is_available(),
    logging_steps=10,
    save_strategy="no",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

trainer.train()

# Save LoRA (produces adapter_config.json + adapter_model.safetensors)
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Done! LoRA files saved in: {OUTPUT_DIR}")
