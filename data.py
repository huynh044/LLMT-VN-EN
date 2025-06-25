import json
import os
import pandas as pd

def add_to_json_file(file_path, data: str):
    """
    Thêm hoặc cập Việt các cặp từ vựng Việt-Anh vào file JSON glossary.
    Tham số:
        file_path (str): Đường dẫn file JSON glossary.
        data (str): Chuỗi các cặp từ vựng dạng 'vn:en:src', phân tách bằng dấu phẩy.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    list_data = data.split(",")
    for text in list_data:
        parts = text.split(":")
        if len(parts) < 2:
            continue  
        vn_text = parts[0].strip()
        en_text = parts[1].strip()
        src_text = parts[2].strip() if len(parts) > 2 else ""

        updated = False
        for item in existing_data:
            if item.get("vn") == vn_text:
                item["en"] = en_text
                item["src"] = src_text
                updated = True
                break
        if not updated:
            existing_data.append({
                "vn": vn_text,
                "en": en_text,
                "src": src_text
            })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

def add_xlsx_to_json(file_path, xlsx_path: str):
    """
    Đọc file Excel và thêm hoặc cập Việt các cặp từ vựng Việt-Anh vào file JSON glossary.
    Tham số:
        file_path (str): Đường dẫn file JSON glossary.
        xlsx_path (str): Đường dẫn file Excel chứa hai cột 'Vietnamese' và 'English'.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    df = pd.read_excel(xlsx_path)
    for index, row in df.iterrows():
        vn_text = row['Vietnamese'].strip()
        en_text = row['English'].strip()
        src_text = row['Source'].strip()
        for item in existing_data:
            if vn_text in item.values():
                item["en"] = en_text
                item["src"] = src_text
                break
        else:
            existing_data.append({
                "vn": vn_text,
                "en": en_text,
                "src": src_text
            })
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)