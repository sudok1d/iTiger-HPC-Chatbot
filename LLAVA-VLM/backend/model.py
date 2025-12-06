import torch
from PIL import Image
from llava.constants import (
    IMAGE_TOKEN_INDEX,
    DEFAULT_IMAGE_TOKEN,
    DEFAULT_IM_START_TOKEN,
    DEFAULT_IM_END_TOKEN,
)
from llava.conversation import conv_templates
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import (
    process_images,
    tokenizer_image_token,
    get_model_name_from_path,
)

disable_torch_init()

MODEL_PATH = "liuhaotian/llava-v1.5-7b"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model_name = get_model_name_from_path(MODEL_PATH)
tokenizer, model, image_processor, context_len = load_pretrained_model(
    MODEL_PATH,
    None,
    model_name,
    load_8bit=False,
    load_4bit=False,
    device=DEVICE,
)

if "llama-2" in model_name.lower():
    conv_mode = "llava_llama_2"
elif "mistral" in model_name.lower():
    conv_mode = "mistral_instruct"
elif "v1.6" in model_name.lower():
    conv_mode = "chatml_direct"
elif "v1" in model_name.lower():
    conv_mode = "llava_v1"
else:
    conv_mode = "llava_v0"

conv_template = conv_templates[conv_mode]


def run_vlm(prompt_text, image: Image.Image | None):
    conv = conv_template.copy()

    image_tensor = None
    image_size = None

    if image is not None:
        image_tensor = process_images([image], image_processor, model.config)
        if isinstance(image_tensor, list):
            image_tensor = [t.to(DEVICE, dtype=torch.float16) for t in image_tensor]
        else:
            image_tensor = image_tensor.to(DEVICE, dtype=torch.float16)
        image_size = image.size
        prompt_text = (
            DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN +
            DEFAULT_IM_END_TOKEN + "\n" + prompt_text
        )

    conv.append_message(conv.roles[0], prompt_text)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()

    input_ids = tokenizer_image_token(
        prompt,
        tokenizer,
        IMAGE_TOKEN_INDEX,
        return_tensors="pt"
    ).unsqueeze(0).to(DEVICE)

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            image_sizes=[image_size] if image_size else None,
            do_sample=False,
            temperature=0.2,
            max_new_tokens=512,
            use_cache=True,
        )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
