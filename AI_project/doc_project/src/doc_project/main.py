import sys
import warnings
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import fitz  # PyMuPDF
import logging
import google.generativeai as genai
import os
from doc_project.crew import BelgeAnalizProjesi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("uvicorn")

app = FastAPI()


class InputData(BaseModel):
    dosya_yolu: str


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

@app.post("/belge_analiz")
def belge_analiz(istek: InputData):
    """
    Hazır dosya yolundan belgeyi okuyup analiz eder.
    """
    
    belge_metni = pdf_oku(istek.dosya_yolu)

    if not belge_metni:
        return {"durum": "hata", "mesaj": "PDF dosyası bulunamadı veya okunamadı."}

    try:
        # AI Ajanlarını çalıştır
        BelgeAnalizProjesi().crew().kickoff(inputs={"belge_adi": os.path.basename(istek.dosya_yolu), "input": belge_metni})
        return {"durum": "başarılı", "mesaj": f"{istek.dosya_yolu} analize gönderildi"}
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}


@app.get("/")
def read_root():
    return {"message": "Langserve API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
