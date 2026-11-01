from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
from datetime import datetime

os.makedirs("data", exist_ok=True)
DB_PATH = "data/app.db"

def get_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu_usage REAL NOT NULL,
            timestamp TEXT NOT NULL
        );""")
    connection.commit()
    connection.close()
    yield

app = FastAPI(title="CPU Metrics Collector API", lifespan=lifespan)

class MetricPayload(BaseModel):
    cpu_usage: float

@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "Active", "message": "Metrics Collector API is working!"}

@app.get("/metrics")
def get_tasks() -> list[dict[str, Any]]:
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, cpu_usage, timestamp FROM metrics ORDER BY id DESC LIMIT 40;")
    rows = cursor.fetchall()
    connection.close()
    return [{"id": row["id"], "cpu_usage": row["cpu_usage"], "timestamp": row["timestamp"]} for row in rows]

@app.post("/metrics")
def create_task(payload: MetricPayload) -> dict[str, Any]:
    connection = get_db()
    cursor = connection.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO metrics (cpu_usage, timestamp) VALUES (?, ?);", (payload.cpu_usage, now_str))
    connection.commit()
    metric_id = cursor.lastrowid
    connection.close()
    return {"id": metric_id, "cpu_usage": payload.cpu_usage, "timestamp": now_str}

@app.delete("/metrics/{metric_id}")
def delete_task(metric_id: int) -> dict[str, str]:
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM metrics WHERE id = ?;", (metric_id,))
    task = cursor.fetchone()
    if task is None:
        connection.close()
        raise HTTPException(status_code=404, detail=f"Metric with id {metric_id} not found.")
    cursor.execute("DELETE FROM metrics WHERE id = ?;", (metric_id,))
    connection.commit()
    connection.close()
    return {"message": f"Task {metric_id} deleted successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)