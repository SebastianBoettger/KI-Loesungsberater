import os

from fastapi import FastAPI
from google import genai
from pydantic import BaseModel


app = FastAPI(title="KI-Lösungsberater")


class Beratungsanfrage(BaseModel):
    anforderung: str


@app.get("/")
def start():
    return {
        "status": "online",
        "message": "KI-Lösungsberater API läuft"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/beratung")
def beratung(anfrage: Beratungsanfrage):
    client = genai.Client(
        vertexai=True,
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location="global"
    )

    prompt = f"""
Du bist ein KI-Lösungsberater für Hardware und technische Lösungen.

Analysiere die folgende Kundenanforderung:
{anfrage.anforderung}

Erstelle einen ersten Lösungsvorschlag mit:
1. erkanntem Bedarf,
2. geeigneten Hardware-Kategorien,
3. wichtigen Auswahlkriterien,
4. möglichen Komponenten,
5. offenen Fragen an den Kunden.

Gib keine erfundenen Produktdaten oder Bestände an.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "anforderung": anfrage.anforderung,
        "empfehlung": response.text
    }
