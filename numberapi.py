from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)  # Ensure Flask app is instantiated correctly and globally

# Helper functions
def is_prime(n):
    """Check if a number is prime."""
    if not isinstance(n, int) or n < 2:  # Prime numbers must be integers ≥ 2
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number."""
    if not isinstance(n, int) or n <= 0:  # No perfect numbers for negatives or non-integers
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    if not isinstance(n, int):  # Armstrong numbers apply to integers only
        return False
    num_str = str(abs(n))
    power = len(num_str)
    return sum(int(d) ** power for d in num_str) == abs(n)

def get_fun_fact(n):
    """Fetch a fun fact about the number from NumbersAPI."""
    try:
        url = f"http://numbersapi.com/{n}/math"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        return "No fact available."
    except requests.exceptions.RequestException:
        return "Fact API unavailable."

@app.route("/", methods=["GET"])
def home():
    """Health check route."""
    return jsonify({"message": "API is working!"}), 200

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify the given number and return properties."""
    number = request.args.get('number')

    if not number:
        return jsonify({"error": "No number provided"}), 400  # Handle missing number

    # Handle invalid numbers (non-numeric values)
    try:
        number = float(number) if '.' in number else int(number)
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

    properties = []
    if isinstance(number, int):
        if is_armstrong(number):
            properties.append("armstrong")
        if is_perfect(number):
            properties.append("perfect")

    properties.append("odd" if number % 2 != 0 else "even")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(abs(number)) if digit.isdigit()),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200  # Return 200 for valid numbers

if __name__ == "__main__":
    app.run(debug=True)
