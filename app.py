from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your OpenRouter API key
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def query_openrouter(user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-70b-instruct",  # Detailed model
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert AI tutor. Provide detailed, clear, educational responses.\n"
                    "- Use headings (like h3) and bullet points.\n"
                    "- Present code examples cleanly in <pre><code> blocks.\n"
                    "- Avoid ** and ``` markdown syntax.\n"
                    "- Format outputs and explanations clearly."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 28000,
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
    app.run(host="0.0.0.0", port=port, debug=False)
