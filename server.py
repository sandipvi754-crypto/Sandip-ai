from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Sandip AI Server is Running! 🤖"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "reply": "কিছু একটা লিখে আমাকে জিজ্ঞাসা করো 😊"
            })

        response = client.responses.create(
            model="gpt-6-luna",
            tools=[
                {"type": "web_search"}
            ],
            instructions="""
তুমি Sandip AI 🤖

ব্যবহারকারী বাংলা বললে বাংলায় উত্তর দেবে।
ব্যবহারকারী হিন্দি বললে হিন্দিতে উত্তর দেবে।

সাম্প্রতিক তথ্য, খবর, বর্তমান দাম,
আবহাওয়া বা Internet-এর তথ্য প্রয়োজন হলে
web search ব্যবহার করবে।

সহজ, বন্ধুত্বপূর্ণ এবং পরিষ্কারভাবে উত্তর দেবে।
""",
            input=message
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        return jsonify({
            "reply": "❌ সমস্যা হয়েছে: " + str(e)
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
