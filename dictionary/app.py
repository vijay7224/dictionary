from flask import Flask, request, jsonify, render_template
import difflib
import os

app = Flask(__name__)

# Load knowledge base
def load_knowledge():
    knowledge_dict = {}

    if not os.path.exists("data.txt"):
        return knowledge_dict

    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                question, answer = line.strip().split("=", 1)
                knowledge_dict[question.strip().lower()] = answer.strip()

    return knowledge_dict


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

        # Exact match
        if user_message in knowledge:
            return jsonify({"reply": knowledge[user_message]})

        # Closest match
        questions = list(knowledge.keys())
        match = difflib.get_close_matches(user_message, questions, n=1, cutoff=0.5)

        if match:
            return jsonify({"reply": knowledge[match[0]]})
        else:
            return jsonify({"reply": "Sorry, information not found in my knowledge base."})

    except Exception as e:
        return jsonify({"reply": "Server error occurred."})
