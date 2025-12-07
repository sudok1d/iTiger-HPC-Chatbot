import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from PIL import Image

MODEL_NAME = "Qwen/Qwen2.5-VL-3B-Instruct"

processor = AutoProcessor.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    low_cpu_mem_usage=True,
    trust_remote_code=True
)

def run_vlm(text, image: Image.Image = None, max_new_tokens=60, temperature=0.1):
    if image is not None:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image.convert("RGB")},
                    {"type": "text", "text": text},
                ],
            }
        ]
    else:
        messages = [
            {"role": "user", "content": [{"type": "text", "text": text}]}
        ]

    prompt = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True  # Changed to True
    )

    image_list = [image.convert("RGB")] if image else None
    inputs = processor(
        text=[prompt],
        images=image_list,
        return_tensors="pt",
    ).to(model.device)

    do_sample = temperature > 0
    temp_val = temperature if temperature > 0 else None
    
    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temp_val,
    )
    
    # Decode only the generated tokens (skip the input prompt)
    generated_ids = output_ids[:, inputs.input_ids.shape[1]:]
    output_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0].strip()
    
    # Take first sentence
    if ". " in output_text:
        output_text = output_text.split(". ")[0].strip(" ?!.") + "."
    else:
        output_text = output_text.strip(" ?!.") + "."
    
    return output_text