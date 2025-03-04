import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import warnings
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import fitz  # PyMuPDF
import logging
import google.generativeai as genai
from doc_project.crew import BelgeAnalizProjesi
from Service.pdf_handler import pdf_oku  # Service katmanından import ettik

from langtrace_python_sdk import langtrace
from dotenv import load_dotenv

# .env dosyasındaki çevre değişkenlerini yükle
load_dotenv()

langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("uvicorn")

app = FastAPI()

class InputData(BaseModel):
    dosya_yolu: str

@app.post("/belge_analiz")
def belge_analiz(istek: InputData):
    """
    Hazır dosya yolundan belgeyi okuyup analiz eder.
    """

    belge_metni = pdf_oku(istek.dosya_yolu)

    if not belge_metni:
        return {"durum": "hata", "mesaj": "PDF dosyası bulunamadı veya okunamadı."}
    try:
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
