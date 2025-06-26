from llama_cpp import Llama
from glossary_handler import parse_translation_output
import time
import os

llm = None
def get_llm():
    """
    Khởi tạo mô hình LLM với cấu hình tối ưu cho CPU.
    Sử dụng mô hình với định dạng GGUF.
    Trả về:
        Llama: Đối tượng mô hình LLM đã khởi tạo.
    """
    global llm
    if llm is not None:
        return llm

    print("Loading model...")
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "model", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    
    print(f"Model path: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    print(f"Model file size: {os.path.getsize(model_path)} bytes")
    
    try:
        llm = Llama(
                model_path=model_path,
                n_threads=4,  # Reduced from 6 to be more conservative
                n_batch=128,  # Reduced from 256 to use less memory
                n_ctx=2048,   # Reduced from 4096 to use less memory
                seed=42,
                f16_kv=False,       
                logits_all=False,
                verbose=False,
                use_mlock=False,  # Changed to False to avoid memory locking issues
                use_mmap=True     # Enable memory mapping for better performance
            )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise
    return llm

def build_prompt(text, glossary):
    """
    Xây dựng prompt cho mô hình LLM để dịch tiếng Việt sang tiếng Anh.
    Sử dụng các cặp từ vựng Việt-Anh trong glossary để ưu tiên dịch thuật ngữ chuyên ngành.
    Tham số:
        text (str): Câu tiếng Việt cần dịch.
        glossary (list): Danh sách các mục glossary từ file JSON.
    Trả về:
        str: Prompt dạng chuỗi cho mô hình LLM.
    """
    glossary_text = "\n".join([f"{entry['vn']} = {entry['en']}" for entry in glossary])
    return f"""Translate the following Vietnamese sentence to English.
    Pay attention to numbers in the text, they should be kept as is.
    Use these preferred translations if these terms appear in the text:
    {glossary_text}

    Vietnamese: {text}

    Then suggest 2-3 very short alternative technical translations.
    Return result in JSON format with two keys only 'translation' and 'alternatives'."""

def translate_with_llm(text, glossary, model):
    """
    Dịch thuật sử dụng mô hình LLM.
    Tham số:
        text (str): Câu tiếng Việt cần dịch.
        glossary (dict): Từ điển các cặp từ vựng Việt-Anh liên quan.
    Trả về:
        dict: Kết quả dịch và các phương án thay thế.
    """
    prompt = build_prompt(text, glossary)
    print("Starting translation (stream)...")
    start = time.time()
    output = ""
    for token in model(prompt, max_tokens=256, stream=True, stop=["}"]):
        output += token["choices"][0]["text"]
        if "}" in output:
            break  
    end = time.time()
    if not output.strip().endswith("}"):
        output += "}"
    result = parse_translation_output(output)
    print(result)
    print(f"Translation completed in {end - start:.2f} seconds.")
    return {"result": result}

