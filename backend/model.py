from transformers import AutoProcessor, AutoModelForVision2Seq
import torch

MODEL_NAME = "Qwen/Qwen2-VL-2B-Instruct"

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForVision2Seq.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

def run_vlm(text):
    inputs = processor(text=[text], return_tensors="pt").to(device)

    output = model.generate(
        **inputs,
        max_new_tokens=128,
        temperature=0.1
    )

    return processor.batch_decode(output, skip_special_tokens=True)[0]
