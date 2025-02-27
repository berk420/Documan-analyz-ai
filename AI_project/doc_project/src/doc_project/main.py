#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# Modül yolunu ekleyin
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc_project.crew import DocProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI()

class InputData(BaseModel):
    topic: str
    current_year: str

@app.get("/")
def read_root():
    return {"message": "Langserve API is running"}

@app.post("/run")
def run(inputs: InputData):
    """
    Run the crew.
    """
    try:
        DocProject().crew().kickoff(inputs=inputs.dict())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/train")
def train(n_iterations: int, filename: str, inputs: InputData):
    """
    Train the crew for a given number of iterations.
    """
    try:
        DocProject().crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs.dict())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/replay")
def replay(task_id: str):
    """
    Replay the crew execution from a specific task.
    """
    try:
        DocProject().crew().replay(task_id=task_id)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/test")
def test(n_iterations: int, openai_model_name: str, inputs: InputData):
    """
    Test the crew execution and returns the results.
    """
    try:
        DocProject().crew().test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs.dict())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
