import os

from fastapi import FastAPI
from google import genai
from pydantic import BaseModel


app = FastAPI(title="KI-Lösungsberater")


class Beratungsanfrage(BaseModel):
    anforderung: str
    einsatzzweck: str
    budget_euro: int
    prioritaeten: list[str]


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

    prioritaeten_text = ", ".join(anfrage.prioritaeten)

    prompt = f"""
Du bist ein KI-Lösungsberater für Hardware und technische Lösungen.

Analysiere die folgende Kundenanfrage.

Allgemeine Anforderung:
{anfrage.anforderung}

Einsatzzweck:
{anfrage.einsatzzweck}

Budget:
{anfrage.budget_euro} Euro

Prioritäten:
{prioritaeten_text}

Erstelle einen strukturierten Lösungsvorschlag mit:

1. Erkanntem Bedarf
2. Empfohlener Lösung
3. Geeigneten Hardware-Kategorien
4. Wichtigen Auswahlkriterien
5. Möglichen Komponenten
6. Begründung der Empfehlungen
7. Möglichen Alternativen
8. Offenen Fragen an den Kunden

Berücksichtige insbesondere den Einsatzzweck, das Budget und die genannten Prioritäten.

Erfinde keine konkreten Produktdaten, Preise, Verfügbarkeiten oder Bestände.
Wenn dafür aktuelle Produktdaten benötigt werden, weise darauf hin.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "kundenanforderung": {
            "anforderung": anfrage.anforderung,
            "einsatzzweck": anfrage.einsatzzweck,
            "budget_euro": anfrage.budget_euro,
            "prioritaeten": anfrage.prioritaeten
        },
        "empfehlung": response.text
    }
