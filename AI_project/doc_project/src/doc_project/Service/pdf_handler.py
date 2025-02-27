import os
import fitz  # PyMuPDF
import logging

logger = logging.getLogger("uvicorn")

def pdf_oku(dosya_yolu: str) -> str:
    """PDF dosyasını aç ve metnini oku"""
    if not os.path.exists(dosya_yolu):
        return None  # Dosya yoksa None döndür
    
    belge_metni = ""

    with fitz.open(dosya_yolu) as pdf:
        for sayfa in pdf:
            belge_metni += sayfa.get_text("text") + "\n"
    
    logger.info(f"PDF başarıyla okundu: {dosya_yolu}")
    return belge_metni.strip()
