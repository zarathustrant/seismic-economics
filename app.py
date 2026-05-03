from flask import Flask, send_file, request, jsonify, session, redirect, render_template_string
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')

# Password (set via environment variable or default)
PASSWORD = os.environ.get('APP_PASSWORD', 'seismic2024')

# Path to the HTML file (anchored to this script's directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, 'app.html')

# Simple password protection decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Login page
LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Seismic Economics</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f766e 0%, #155e75 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            width: 300px;
        }
        h2 {
            margin: 0 0 20px 0;
            color: #0f766e;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            margin-bottom: 15px;
            font-size: 14px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #0f766e;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
        }
        button:hover {
            background: #155e75;
        }
        .error {
            color: #dc2626;
            font-size: 13px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🌊 Seismic Economics</h2>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <input type="password" name="password" placeholder="Enter password" autofocus>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['authenticated'] = True
            return redirect('/')
        return render_template_string(LOGIN_PAGE, error='Invalid password')
    return render_template_string(LOGIN_PAGE)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect('/login')

@app.route('/')
@require_auth
def index():
    """Serve the main HTML file"""
    return send_file(HTML_FILE)

@app.route('/api/save', methods=['POST'])
@require_auth
def save():
    """Save the updated HTML file"""
    try:
        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            return jsonify({'success': False, 'error': 'Invalid JSON payload'}), 400

        html_content = data.get('html')

        if not html_content:
            return jsonify({'success': False, 'error': 'No HTML content provided'}), 400

        # Save to file
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return jsonify({'success': True, 'message': 'File saved successfully'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
