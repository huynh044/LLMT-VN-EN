# LLMT-VN-EN - Vietnamese-English Translation Application

A powerful web-based translation application that leverages Large Language Models (LLM) for Vietnamese-English translation with OCR capabilities, glossary management, and translation history tracking.

## Features

- **LLM-Powered Translation**: Uses Mistral-7B-Instruct-v0.2 model for high-quality Vietnamese-English translation
- **OCR Integration**: Extract text from images using EasyOCR with automatic rotation detection
- **Glossary Management**: Upload and manage custom glossaries for domain-specific translations
- **Translation History**: Track and save all translation activities
- **Web Interface**: Modern, responsive web UI built with Bootstrap
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Semantic Similarity**: Intelligent glossary term matching using similarity algorithms

## Technology Stack

- **Backend**: FastAPI, Python 3.11.13
- **LLM**: Mistral-7B-Instruct-v0.2 (GGUF format)
- **OCR**: EasyOCR
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Processing**: NumPy, OpenCV, Pandas
- **Model Management**: llama-cpp-python

## Prerequisites

- Python 3.11.13 or higher
- Sufficient RAM for LLM model (recommended: 8GB+)
- GPU (optional, for better performance)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LLMT-VN-EN
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the LLM model**
   - Download from: [Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/blob/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf)
   - Place in the `model/` directory

4. **Start the application**
   ```bash
   python main.py
   ```

5. **Access the web interface**
   - Open your browser and navigate to `http://localhost:8000`

## Project Structure

```
LLMT-VN-EN/
├── main.py                 # FastAPI application entry point
├── llm_handler.py          # LLM model management and translation logic
├── glossary_handler.py     # Glossary management and term extraction
├── history_handler.py      # Translation history tracking
├── data.py                 # Data processing utilities
├── test_similarity.py      # Testing utilities for similarity functions
├── requirements.txt        # Python dependencies
├── data/
│   └── glossary.json      # Glossary storage
├── hist/
│   └── translation_history.json  # Translation history
├── model/                  # LLM model files
└── static/
    ├── index.html         # Web interface
    ├── main.js           # Frontend JavaScript
    └── style.css         # Styling
```

## API Endpoints

- `POST /api/translate` - Translate text from Vietnamese to English
- `POST /api/ocr` - Extract text from uploaded images
- `POST /api/upload-glossary` - Upload custom glossary files
- `GET /api/history` - Retrieve translation history
- `GET /` - Serve the web interface

## Data Format

The application supports the following data formats:

### Glossary Format (JSON)
```json
{
  "term_id": {
    "vietnamese": "Vietnamese term",
    "english": "English translation",
    "source": "Context or source of translation"
  }
}
```

### Translation History Format
```json
{
  "timestamp": "2025-07-09T12:00:00Z",
  "input": "Vietnamese text",
  "output": "English translation",
  "relevant_glossary": ["term1", "term2"]
}
```

## Usage Examples

### Text Translation
1. Enter Vietnamese text in the input area
2. Click "Translate" to get English translation
3. View results with applied glossary terms

### OCR Translation
1. Click "OCR" to upload an image
2. The system extracts text automatically
3. Translate the extracted text

### Glossary Management
1. Click "Add Glossary" to upload .xlsx or .txt files
2. Custom terms improve translation accuracy
3. View glossary usage in translation history

## Configuration

### Model Configuration
- Model path: `model/mistral-7b-instruct-v0.2.Q4_K_M.gguf`
- Similarity threshold: 0.3 (configurable)
- Max glossary terms: 10 per translation

### OCR Configuration
- Supported languages: Vietnamese, English
- Auto-rotation: Enabled
- Supported formats: JPG, PNG, JPEG, WebP

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Model Information

**LLM Model**: Mistral-7B-Instruct-v0.2-GGUF
- **Source**: [TheBloke/Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
- **Format**: GGUF (GPT-Generated Unified Format)
- **Quantization**: Q4_K_M (4-bit quantization, medium quality)

## Support

If you encounter any issues or have questions, please:
1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Provide error logs and system information

---

*Built with love using FastAPI, Mistral LLM, and modern web technologies*
