from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_product(url):
    try:
        res = requests.get(url, timeout=10)

        if res.status_code == 404:
            return "NOT_FOUND"

        text = res.text.lower()

        if "product not found" in text:
            return "NOT_FOUND"

        soup = BeautifulSoup(res.text, "html.parser")

        if not soup.find("h1"):
            return "NOT_FOUND"

        return "FOUND"

    except:
        return "ERROR"

@app.get("/check")
def check(url: str):
    return {"result": check_product(url)}
