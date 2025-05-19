import random
import asyncio
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/process", methods=["POST"])
async def process():
    delay = random.uniform(1, 3)
    await asyncio.sleep(delay)
    return f"Took {delay:.2f} seconds"