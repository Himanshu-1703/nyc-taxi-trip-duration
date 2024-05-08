from fastapi import FastAPI
import uvicorn
from data_models import PredictionDataset


if __name__ == "__main__":
    uvicorn.run(app='app:app',host="127.0.0.1")
    
    