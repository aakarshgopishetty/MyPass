from flask import Flask, render_template, request, jsonify
import zxcvbn  # Password strength checker

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-password-strength', methods=['POST'])
def check_password_strength():
    data = request.get_json()
    password = data['password']
    result = zxcvbn.password_strength(password)
    
    response = {
        "strength": "Very Weak" if result["score"] == 0 else "Weak" if result["score"] == 1 else "Fair" if result["score"] == 2 else "Strong",
        "suggestions": result["feedback"]["suggestions"]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
