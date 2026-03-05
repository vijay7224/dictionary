from flask import Flask, request, jsonify, render_template
import difflib
import os

app = Flask(__name__)

# Load knowledge base
def load_knowledge():
    if not os.path.exists("data.txt"):
        return []
    with open("data.txt", "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f.readlines()]

knowledge = load_knowledge()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "Please send a valid message."})

        user_message = data["message"].strip().lower()

        if user_message == "":
            return jsonify({"reply": "Message cannot be empty."})

        # Find closest match
        match = difflib.get_close_matches(
            user_message,
            knowledge,
            n=1,
            cutoff=0.4  # similarity threshold
        )

        if match:
            reply = match[0]
        else:
            reply = "Sorry, information not found in my knowledge base."

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Server error occurred."})

