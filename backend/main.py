from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Initialisation de l'API
app = FastAPI(
    title="Supervision API",
    description="API de réception des télémétries et alertes serveurs",
    version="1.0.0"
)

# POO & Validation des données avec Pydantic
class ServerAlert(BaseModel):
    server_name: str = Field(..., example="SRV-RADAR-01")
    cpu_usage: float = Field(..., ge=0.0, le=100.0, example=85.5)
    status: str = Field(..., example="WARNING")
    timestamp: datetime = Field(default_factory=datetime.now)

# BDD temporaire (en mémoire)
alerts_db: List[ServerAlert] = []

@app.post("/api/alerts", response_model=ServerAlert, status_code=201)
def trigger_alert(alert: ServerAlert):
    """
    Reçoit une nouvelle alerte d'un serveur et la stocke.
    """
    alerts_db.append(alert)
    return alert

@app.get("/api/alerts", response_model=List[ServerAlert])
def get_all_alerts():
    """
    Retourne la liste de toutes les alertes enregistrées.
    """
    return alerts_db