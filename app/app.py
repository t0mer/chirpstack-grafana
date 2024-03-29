import os
import uvicorn
import requests
from pathlib import Path
from loguru import logger
from typing import Annotated
from fastapi import FastAPI, Request, Depends

app = FastAPI(
    docs_url=None, # Disable docs (Swagger UI)
    redoc_url=None, # Disable redoc
)

@app.post("/", include_in_schema=False, status_code=201)
async def webhook(request: Request, event:str = ""):
    data = await request.json()
    # logger.info(str(data))
# Append-adds at last
    if event == "up":
        with open("up.json", "a") as messages:
            messages.write(str(data).replace("'",'"') + "\n")
        return "ok"
    
    if event == "status":
        with open("status.json", "a") as messages:
            messages.write(str(data).replace("'",'"') + "\n")
        return "ok"
    
    if event == "join":
        with open("join.json", "a") as messages:
            messages.write(str(data).replace("'",'"') + "\n")
        return "ok"

        
if __name__ == '__main__':
    logger.info("Whatsapp Webhook is up and running")
    uvicorn.run(app, host="0.0.0.0", port=8213)