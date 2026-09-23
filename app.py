from flask import Flask, render_template, request
import serial
import time
import threading
from collections import deque

print_queue = deque()
requests = {}
app = Flask(__name__)
stm32 = serial.Serial("COM4", 9600, timeout=2)



replacements = {
    # Smart quotes / apostrophes
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',

    # Dashes
    "\u2013": "-",      # en dash
    "\u2014": "-",      # em dash

    # Ellipsis
    "\u2026": "...",

    # Spaces
    "\u00a0": " ",      # non-breaking space
    "\u2009": " ",      # thin space
    "\u202f": " ",      # narrow no-break space

    # Common symbols
    "\u2022": "*",      # bullet
    "\u00b7": ".",      # middle dot
    "\u00a9": "(c)",    # copyright
    "\u00ae": "(R)",    # registered
    "\u2122": "(TM)",   # trademark
    "\u00b0": " degrees ",
    "\u00d7": "x",      # multiplication
    "\u00f7": "/",      # division

    # Common mathematical comparisons
    "\u2264": "<=",
    "\u2265": ">=",
    "\u2260": "!=",

    # Arrows
    "\u2192": "->",
    "\u2190": "<-",
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    message = request.form["message"]
    
    ip = request.remote_addr

    message, error = validation(message)
    if error:
        return error

    if not rate_limiting(ip):
        return "Cannot send more messages"

    if len(print_queue) >= 10:
        return "Print Queue is full"

    print_queue.append(message)

    return "Message received!"


def printer_worker():
    while True:
        if print_queue:
            message = print_queue.popleft()

            stm32.write(
                (message + "\x04").encode()
            )

def validation(message):
    if not message:
        return None, "Please send a different message."

    if len(message) > 500:
        return None, "Message too long"

    for old, new in replacements.items():
        message = message.replace(old, new)

    if not message.isascii():
        return None, "Message contains unsupported characters."

    return message, None

def rate_limiting(ip):
    now = time.time()

    timestamps = requests.get(ip, [])

    timestamps = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < 60
    ]

    # Per-IP limit
    if len(timestamps) >= 5:
        return False

    # Global limit
    total_requests = 0

    for value in requests.values():
        total_requests += len(value)

    if total_requests >= 20:
        return False

    # Request passed both limits
    timestamps.append(now)
    requests[ip] = timestamps

    return True


if __name__ == "__main__":
    worker = threading.Thread(target=printer_worker, daemon=True)
    worker.start()
    app.run(debug=True, use_reloader=False)