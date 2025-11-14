import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from config import MODEL_ID

@st.cache_resource
def load_model():

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=bnb_config,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )

        model.config.use_cache = False

        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def generate_text(system_prompt, user_prompt, model, tokenizer, llm_params):

    if model is None or tokenizer is None:
        return "Error: Model not loaded."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    model_inputs = encodeds.to(model.device)
    input_token_length = model_inputs.shape[1]

    try:
        generated_ids = model.generate(
            model_inputs,
            max_new_tokens=llm_params.get("max_new_tokens", 4096),
            temperature=llm_params.get("temperature", 0.7),
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        new_token_ids = generated_ids[0, input_token_length:]

        reply = tokenizer.decode(new_token_ids, skip_special_tokens=True)

        return reply.strip()

    except Exception as e:
        return f"Error during text generation: {e}"
