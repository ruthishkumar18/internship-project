from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def query_openrouter(user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert AI tutor. Respond clearly and neatly.\n"
                    "- Use <h3> for main headings, <h4> for subheadings.\n"
                    "- Use <ul><li> for bullet points.\n"
                    "- Use <pre><code> for code blocks (with correct indentation).\n"
                    "- Do NOT use ** or markdown code fences.\n"
                    "- Format so it looks like ChatGPT replies (structured and clean)."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 6000,
        "temperature": 0.6,
        "top_p": 1
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_reply():
    user_msg = request.json.get("msg", "")
    if not user_msg.strip():
        return jsonify({"reply": "Please enter a valid question."})
    
    bot_reply = query_openrouter(user_msg)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
