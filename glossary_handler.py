import json
import re
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
    
GLOSSARY_PATH = "data/glossary.json"
def parse_translation_output(raw_output):
    """
    Parse kết quả trả về từ mô hình LLM sang dict.
    Tham số:
        raw_output (str): Chuỗi kết quả trả về từ LLM.
    Trả về:
        dict: Kết quả dịch và các phương án thay thế.
    """
    try:
        json_text = re.search(r"\{.*?\}", raw_output, re.DOTALL).group(0)
        return json.loads(json_text)
    except:
        return {
            "translation": raw_output.strip(),
            "alternatives": []
        }

def load_glossary():
    """
    Đọc file glossary.json và trả về từ điển các cặp từ vựng Việt-Anh.
    Trả về:
        list: Danh sách các mục glossary từ file JSON.
    """
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        glossary_list = json.load(f)
    return glossary_list

def difflib_similarity(text1, text2):
    """
    Tính độ tương đồng giữa hai chuỗi sử dụng difflib.
    Tham số:
        text1, text2 (str): Hai chuỗi cần so sánh.
    Trả về:
        float: Điểm tương đồng từ 0.0 đến 1.0.
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def extract_tfidf_features(texts):
    """
    Trích xuất đặc trưng TF-IDF từ danh sách văn bản.
    Tham số:
        texts (list): Danh sách các văn bản.
    Trả về:
        tuple: (vectorizer, tfidf_matrix) - Vectorizer và ma trận TF-IDF.
    """
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),  # Unigrams và bigrams
        max_features=1000,
        stop_words=None
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

def calculate_cosine_similarity(vector1, vector2):
    """
    Tính cosine similarity giữa hai vector.
    Tham số:
        vector1, vector2: Hai vector TF-IDF.
    Trả về:
        float: Điểm cosine similarity từ 0.0 đến 1.0.
    """
    similarity = cosine_similarity(vector1, vector2)
    return similarity[0][0]

def extract_relevant_terms(text, glossary, similarity_threshold=0.3, max_terms=10):
    """
    Lọc ra các mục glossary có từ vựng liên quan sử dụng TF-IDF, difflib và cosine similarity.
    Tham số:
        text (str): Câu tiếng Việt cần dịch.
        glossary (list): Danh sách glossary từ file JSON.
        similarity_threshold (float): Ngưỡng điểm tương đồng (0.0-1.0).
        max_terms (int): Số lượng terms tối đa trả về.
    Trả về:
        list: Danh sách các mục glossary liên quan được sắp xếp theo độ ưu tiên.
    """
    if not glossary or not text.strip():
        return []
    
    # Chuẩn bị dữ liệu
    text_lower = text.lower().strip()
    vn_terms = [entry["vn"] for entry in glossary]
    
    # Tạo corpus bao gồm text đầu vào và tất cả terms trong glossary
    all_texts = [text_lower] + [term.lower() for term in vn_terms]
    
    # Trích xuất đặc trưng TF-IDF
    try:
        vectorizer, tfidf_matrix = extract_tfidf_features(all_texts)
        input_vector = tfidf_matrix[0:1]  # Vector của text đầu vào
        term_vectors = tfidf_matrix[1:]   # Vector của các terms
    except:
        # Fallback nếu TF-IDF thất bại
        return extract_relevant_terms_simple(text, glossary, similarity_threshold, max_terms)
    
    scored_terms = []
    
    for i, entry in enumerate(glossary):
        vn_term = entry["vn"].lower()
        total_score = 0.0
        
        # 1. Kiểm tra exact match (điểm cao nhất)
        if vn_term in text_lower:
            total_score += 1.0
        
        # 2. Tính difflib similarity
        difflib_score = difflib_similarity(text_lower, vn_term)
        total_score += difflib_score * 0.4
        
        # 3. Tính cosine similarity từ TF-IDF vectors
        if i < term_vectors.shape[0]:
            term_vector = term_vectors[i:i+1]
            cosine_score = calculate_cosine_similarity(input_vector, term_vector)
            total_score += cosine_score * 0.6
        
        # Normalize điểm về khoảng [0, 1]
        final_score = min(total_score / 2.0, 1.0)
        
        # Thêm vào kết quả nếu vượt ngưỡng
        if final_score >= similarity_threshold:
            scored_terms.append((entry, final_score))
    
    # Sắp xếp theo điểm số giảm dần
    scored_terms.sort(key=lambda x: x[1], reverse=True)
    
    # Trả về top terms
    return [term[0] for term in scored_terms[:max_terms]]

def extract_relevant_terms_simple(text, glossary, similarity_threshold=0.5, max_terms=10):
    """
    Phương pháp dự phòng sử dụng chỉ difflib khi TF-IDF thất bại.
    """
    text_lower = text.lower().strip()
    scored_terms = []
    
    for entry in glossary:
        vn_term = entry["vn"].lower()
        
        # Exact match
        if vn_term in text_lower:
            scored_terms.append((entry, 1.0))
            continue
        
        # Difflib similarity
        difflib_score = difflib_similarity(text_lower, vn_term)
        if difflib_score >= similarity_threshold:
            scored_terms.append((entry, difflib_score))
    
    # Sắp xếp và trả về
    scored_terms.sort(key=lambda x: x[1], reverse=True)
    return [term[0] for term in scored_terms[:max_terms]]
