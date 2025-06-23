# import important libraries
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import joblib
from datetime import datetime

# Initialize the FastAPI application
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the model
with open("phishing.pkl", "rb") as f:
    phish_model = joblib.load(f)

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/predict")
async def predict(url: str = Form(...)):
    X_predict = [url]
    prediction = phish_model.predict(X_predict)[0]
    result = "This is a Phishing URL" if prediction == 'bad' else "This is not a Phishing URL"
    detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    return JSONResponse(content={"result": result,"Detection time":detection_time })
