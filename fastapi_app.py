import asyncio
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Enable CORS for all origins and methods (fine for local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow any origin (you can restrict this later)
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)

@app.post("/process", response_class=PlainTextResponse)
async def process():
    # simulate a non-blocking async I/O or network call
    delay = random.uniform(1,3)
    await asyncio.sleep(delay)
    return f"Took {delay:.2f} seconds"
