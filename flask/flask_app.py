import random
import time
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This line enables CORS for all routes

@app.route("/process", methods=["POST"])
def process():
    # simulate a blocking I/O or network call
    delay = random.uniform(1,3)
    time.sleep(delay)
    return f"Took {delay:.2f} seconds"

if __name__ == "__main__":
    # dev server (single-threaded by default)
    app.run(host="0.0.0.0", port=5050)
