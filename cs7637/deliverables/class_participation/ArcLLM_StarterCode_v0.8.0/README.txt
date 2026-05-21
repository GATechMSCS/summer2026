How to Use It (Student Instructions)

Unzip the model zip file you downloaded (e.g., phi-4.zip → folder phi-4 etc.)
Put your trained LoRA folder (e.g., ./my_lora/) in the same directory
Update the model_name.txt file (uncomment the 1 line to match your model)

Update the two paths at the top of the script:

MODEL_FOLDER = "./phi-4" (or your model of choice)
LORA_FOLDER = "./my_lora" (or None to test without LoRA ~ base model only)

start your environment up then:
Run: python ArcDriver.py

Check Milestone_Results.csv for your scores on the training problems (with/without LoRA)