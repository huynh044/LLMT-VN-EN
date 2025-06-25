#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script để kiểm tra hoạt động của hệ thống similarity matching.
"""

from glossary_handler import (
    extract_relevant_terms, 
    difflib_similarity,
    extract_tfidf_features,
    calculate_cosine_similarity
)
import json

def create_test_glossary():
    """Tạo glossary test"""
    return [
        {"vn": "hệ thống", "en": "system"},
        {"vn": "máy học", "en": "machine learning"},
        {"vn": "học máy", "en": "machine learning"},
        {"vn": "thuật toán", "en": "algorithm"},
        {"vn": "phân loại", "en": "classification"},
        {"vn": "deep learning", "en": "deep learning"},
        {"vn": "mạng neural", "en": "neural network"},
        {"vn": "trí tuệ nhân tạo", "en": "artificial intelligence"},
        {"vn": "xử lý ngôn ngữ tự nhiên", "en": "natural language processing"},
        {"vn": "dữ liệu", "en": "data"},
        {"vn": "mô hình", "en": "model"}
    ]

def test_difflib_similarity():
    """Test hàm difflib similarity"""
    print("=== TEST DIFFLIB SIMILARITY ===")
    
    test_cases = [
        ("máy học", "học máy"),
        ("hệ thống", "hệ thống máy tính"),
        ("deep learning", "deep learning neural"),
        ("thuật toán", "algorithm")
    ]
    
    for text1, text2 in test_cases:
        score = difflib_similarity(text1, text2)
        print(f"'{text1}' vs '{text2}': {score:.3f}")
    print()

def test_tfidf_cosine():
    """Test TF-IDF và cosine similarity"""
    print("=== TEST TF-IDF COSINE SIMILARITY ===")
    
    texts = [
        "hệ thống máy học sử dụng thuật toán",
        "hệ thống",
        "máy học", 
        "thuật toán",
        "deep learning",
        "mạng neural"
    ]
    
    try:
        vectorizer, tfidf_matrix = extract_tfidf_features(texts)
        
        # So sánh text đầu tiên với các text khác
        input_vector = tfidf_matrix[0:1]
        
        for i in range(1, len(texts)):
            term_vector = tfidf_matrix[i:i+1]
            similarity = calculate_cosine_similarity(input_vector, term_vector)
            print(f"'{texts[0]}' vs '{texts[i]}': {similarity:.3f}")
            
    except Exception as e:
        print(f"Lỗi TF-IDF: {e}")
    print()

def test_extract_relevant_terms():
    """Test hàm extract_relevant_terms chính"""
    print("=== TEST EXTRACT RELEVANT TERMS ===")
    
    test_texts = [
        "Hệ thống máy học này sử dụng thuật toán phân loại",
        "Deep learning là một phần của trí tuệ nhân tạo", 
        "Mạng neural được sử dụng trong xử lý ngôn ngữ tự nhiên",
        "Mô hình học máy cần dữ liệu để training"
    ]
    
    glossary = create_test_glossary()
    
    for text in test_texts:
        print(f"\nText: '{text}'")
        
        # Test với threshold khác nhau
        for threshold in [0.2, 0.3, 0.5]:
            relevant_terms = extract_relevant_terms(
                text, glossary, 
                similarity_threshold=threshold, 
                max_terms=5
            )
            
            print(f"  Threshold {threshold}: {len(relevant_terms)} terms")
            for term in relevant_terms:
                print(f"    - {term['vn']} -> {term['en']}")

def test_with_sample_data():
    """Test với dữ liệu thực tế từ file glossary.json"""
    print("\n=== TEST WITH REAL GLOSSARY DATA ===")
    
    try:
        with open("data/glossary.json", "r", encoding="utf-8") as f:
            real_glossary = json.load(f)
        
        test_text = "Hệ thống máy học sử dụng thuật toán deep learning"
        
        relevant_terms = extract_relevant_terms(
            test_text, real_glossary, 
            similarity_threshold=0.3, 
            max_terms=8
        )
        
        print(f"Text: '{test_text}'")
        print(f"Found {len(relevant_terms)} relevant terms:")
        for term in relevant_terms:
            print(f"  - {term['vn']} -> {term['en']}")
            
    except FileNotFoundError:
        print("File data/glossary.json không tồn tại")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    print("TESTING SIMILARITY SYSTEM")
    print("=" * 50)
    
    test_difflib_similarity()
    test_tfidf_cosine()
    test_extract_relevant_terms()
    test_with_sample_data()
    
    print("\n" + "=" * 50)
    print("TEST COMPLETED")
