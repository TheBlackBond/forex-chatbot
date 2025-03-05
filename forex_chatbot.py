if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

import json
import random
import requests
import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Keys and Endpoints (Replace with your own keys if needed)
FOREX_API_URL = "https://www.alphavantage.co/query"
FOREX_API_KEY = "demo"  # Replace with your own Alpha Vantage API key
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Sample responses for forex education
responses = {
    "greeting": ["Hello! How can I help with your forex learning today?", "Hi there! Ready to level up your forex knowledge?"],
    "what is forex": ["Forex, or foreign exchange, is the global market for trading currencies."],
    "pip": ["A pip is the smallest price move that a currency pair can make."],
    "leverage": ["Leverage in forex allows traders to control a larger position with a smaller amount of capital."],
    "stop loss": ["A stop loss is an order placed to sell a security when it reaches a certain price to limit losses."],
    "lot size": ["Lot size refers to the number of units of a currency pair that you are trading."],
    "thank you": ["You're welcome! Keep learning and happy trading!", "Anytime! Stay consistent in your forex journey!"],
    "default": ["I'm not sure about that. Can you rephrase or ask another forex-related question?"]
}

# Function to fetch forex rates
def get_forex_rate(pair):
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": pair[:3],
        "to_currency": pair[3:],
        "apikey": FOREX_API_KEY
    }
    response = requests.get(FOREX_API_URL, params=params)
    data = response.json()
    if "Realtime Currency Exchange Rate" in data:
        return f"The current rate for {pair} is {data['Realtime Currency Exchange Rate']['5. Exchange Rate']}"
    return "Sorry, I couldn't fetch the forex rate right now."

# Function to fetch crypto prices
def get_crypto_price(crypto):
    params = {"ids": crypto.lower(), "vs_currencies": "usd"}
    response = requests.get(CRYPTO_API_URL, params=params)
    data = response.json()
    if crypto.lower() in data:
        return f"The current price of {crypto.upper()} is ${data[crypto.lower()]['usd']}"
    return "Sorry, I couldn't fetch the crypto price right now."

# Function to generate chatbot response
def chatbot_response(user_input):
    tokens = word_tokenize(user_input.lower())
    
    for key in responses.keys():
        if key in tokens:
            return random.choice(responses[key])
    
    if len(user_input) == 6 and user_input[:3].isalpha() and user_input[3:].isalpha():
        return get_forex_rate(user_input.upper())
    
    if user_input.lower() in ["bitcoin", "ethereum", "btc", "eth"]:
        return get_crypto_price(user_input.lower())
    
    return random.choice(responses["default"])

# Flask route for chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Please enter a message."})
    
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
