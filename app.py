from flask import Flask, send_file, request, jsonify, session, redirect, render_template_string
from functools import wraps
from pymongo import MongoClient, ASCENDING, DESCENDING, UpdateOne
from pymongo.errors import PyMongoError
import os
import re
import json
import time

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')

# Password (set via environment variable or default)
PASSWORD = os.environ.get('APP_PASSWORD', 'seismic2024')

# Path to the HTML file (anchored to this script's directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, 'app.html')

MONGODB_URI = os.environ.get('MONGODB_URI', '').strip()
MONGO_DB_NAME = os.environ.get('MONGODB_DB', 'seismic_economics')
MONGO_COLLECTION = os.environ.get('MONGODB_COLLECTION', 'projects')

mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000) if MONGODB_URI else None
projects_col = mongo_client[MONGO_DB_NAME][MONGO_COLLECTION] if mongo_client else None
indexes_ready = False
migration_checked = False


def now_ms():
    return int(time.time() * 1000)


def generate_project_id():
    return f"p{now_ms():x}"


def clean_name(value):
    text = str(value or '').strip()
    return text[:120] if text else 'Untitled Project'


def clean_project_id(value):
    text = str(value or '').strip()
    if not text:
        return generate_project_id()
    safe = ''.join(ch for ch in text if ch.isalnum() or ch in ('-', '_'))
    return safe[:60] or generate_project_id()


def parse_embedded_projects():
    if not os.path.exists(HTML_FILE):
        return []
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    match = re.search(
        r'<script type="application/json" id="embedded-projects-data">([\s\S]*?)</script>',
        html,
        re.IGNORECASE,
    )
    if not match:
        return []

    raw = match.group(1).strip()
    if not raw:
        return []

    payload = json.loads(raw)
    projects = payload.get('projects') if isinstance(payload, dict) else {}
    if not isinstance(projects, dict):
        return []

    items = []
    for key, proj in projects.items():
        if not isinstance(proj, dict):
            continue
        project_data = proj.get('data') if isinstance(proj.get('data'), dict) else {}
        pid = clean_project_id(proj.get('id') or key)
        name = clean_name(proj.get('name') or project_data.get('projectInputs', {}).get('projectName'))
        created_at = int(proj.get('createdAt') or now_ms())
        updated_at = int(proj.get('updatedAt') or created_at)
        items.append({
            '_id': pid,
            'name': name,
            'data': project_data,
            'createdAt': created_at,
            'updatedAt': updated_at,
        })

    return items


def ensure_db_ready():
    global indexes_ready, migration_checked

    if projects_col is None:
        return False, 'MONGODB_URI is not configured on the server.'

    try:
        if not indexes_ready:
            projects_col.create_index([('updatedAt', DESCENDING)])
            projects_col.create_index([('createdAt', ASCENDING)])
            indexes_ready = True

        if not migration_checked:
            has_any = projects_col.count_documents({}, limit=1) > 0
            if not has_any:
                seed = parse_embedded_projects()
                if seed:
                    projects_col.insert_many(seed, ordered=False)
            migration_checked = True

        return True, None
    except PyMongoError as exc:
        return False, str(exc)


def sanitize_project_payload(payload, *, require_data=False):
    if not isinstance(payload, dict):
        return None, 'Payload must be a JSON object.'

    name = clean_name(payload.get('name')) if ('name' in payload or require_data) else None
    project_data = payload.get('data')

    if require_data and not isinstance(project_data, dict):
        return None, 'Project data must be an object.'
    if project_data is not None and not isinstance(project_data, dict):
        return None, 'Project data must be an object.'

    out = {
        'name': name,
        'data': project_data,
    }
    return out, None


def serialize_project_meta(doc):
    return {
        'id': doc['_id'],
        'name': doc.get('name', 'Untitled Project'),
        'createdAt': int(doc.get('createdAt') or now_ms()),
        'updatedAt': int(doc.get('updatedAt') or now_ms()),
    }


def serialize_project_full(doc):
    item = serialize_project_meta(doc)
    item['data'] = doc.get('data') if isinstance(doc.get('data'), dict) else {}
    return item


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


@app.route('/api/projects', methods=['GET'])
@require_auth
def list_projects():
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    docs = list(projects_col.find({}, {'data': 0}).sort('updatedAt', DESCENDING))
    return jsonify({'success': True, 'projects': [serialize_project_meta(d) for d in docs]})


@app.route('/api/projects/<project_id>', methods=['GET'])
@require_auth
def get_project(project_id):
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    pid = clean_project_id(project_id)
    doc = projects_col.find_one({'_id': pid})
    if not doc:
        return jsonify({'success': False, 'error': 'Project not found'}), 404

    return jsonify({'success': True, 'project': serialize_project_full(doc)})


@app.route('/api/projects', methods=['POST'])
@require_auth
def create_project():
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    payload = request.get_json(silent=True) or {}
    cleaned, err = sanitize_project_payload(payload, require_data=True)
    if err:
        return jsonify({'success': False, 'error': err}), 400

    pid = clean_project_id(payload.get('id'))
    ts = now_ms()

    if projects_col.find_one({'_id': pid}, {'_id': 1}):
        pid = generate_project_id()

    doc = {
        '_id': pid,
        'name': cleaned['name'],
        'data': cleaned['data'],
        'createdAt': int(payload.get('createdAt') or ts),
        'updatedAt': int(payload.get('updatedAt') or ts),
    }

    try:
        projects_col.insert_one(doc)
    except PyMongoError as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500

    return jsonify({'success': True, 'project': serialize_project_full(doc)}), 201


@app.route('/api/projects/<project_id>', methods=['PUT'])
@require_auth
def update_project(project_id):
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    payload = request.get_json(silent=True) or {}
    cleaned, err = sanitize_project_payload(payload, require_data=False)
    if err:
        return jsonify({'success': False, 'error': err}), 400

    update = {'updatedAt': now_ms()}
    if cleaned['name'] is not None:
        update['name'] = cleaned['name']
    if cleaned['data'] is not None:
        update['data'] = cleaned['data']

    if len(update) == 1:
        return jsonify({'success': False, 'error': 'No fields to update'}), 400

    pid = clean_project_id(project_id)

    result = projects_col.update_one({'_id': pid}, {'$set': update})
    if result.matched_count == 0:
        return jsonify({'success': False, 'error': 'Project not found'}), 404

    doc = projects_col.find_one({'_id': pid})
    return jsonify({'success': True, 'project': serialize_project_full(doc)})


@app.route('/api/projects/<project_id>', methods=['DELETE'])
@require_auth
def delete_project(project_id):
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    docs = list(projects_col.find({}, {'_id': 1}))
    if len(docs) <= 1:
        return jsonify({'success': False, 'error': 'Cannot delete the only project.'}), 400

    pid = clean_project_id(project_id)
    result = projects_col.delete_one({'_id': pid})
    if result.deleted_count == 0:
        return jsonify({'success': False, 'error': 'Project not found'}), 404

    return jsonify({'success': True})


@app.route('/api/projects/export', methods=['GET'])
@require_auth
def export_projects():
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    docs = list(projects_col.find({}).sort('updatedAt', DESCENDING))
    return jsonify({'success': True, 'projects': [serialize_project_full(d) for d in docs]})


@app.route('/api/projects/import', methods=['POST'])
@require_auth
def import_projects():
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    payload = request.get_json(silent=True) or {}
    mode = str(payload.get('mode') or 'merge').lower()
    raw_projects = payload.get('projects')

    if not isinstance(raw_projects, list):
        return jsonify({'success': False, 'error': 'projects must be an array.'}), 400
    if len(raw_projects) == 0:
        return jsonify({'success': False, 'error': 'No projects provided.'}), 400
    if len(raw_projects) > 500:
        return jsonify({'success': False, 'error': 'Too many projects in one import.'}), 400

    ts = now_ms()
    ops = []
    imported = 0

    for item in raw_projects:
        if not isinstance(item, dict):
            continue
        data = item.get('data')
        if not isinstance(data, dict):
            continue

        pid = clean_project_id(item.get('id'))
        name = clean_name(item.get('name'))
        created_at = int(item.get('createdAt') or ts)
        updated_at = int(item.get('updatedAt') or ts)

        ops.append(UpdateOne(
            {'_id': pid},
            {'$set': {
                'name': name,
                'data': data,
                'updatedAt': updated_at,
            }, '$setOnInsert': {
                'createdAt': created_at,
            }},
            upsert=True,
        ))
        imported += 1

    if imported == 0:
        return jsonify({'success': False, 'error': 'No valid projects in import payload.'}), 400

    try:
        if mode == 'replace':
            projects_col.delete_many({})
        projects_col.bulk_write(ops, ordered=False)
    except PyMongoError as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500

    return jsonify({'success': True, 'imported': imported, 'mode': mode})


@app.route('/api/save', methods=['POST'])
@require_auth
def save_deprecated():
    """Deprecated endpoint retained for backward compatibility."""
    return jsonify({
        'success': True,
        'deprecated': True,
        'message': 'Deprecated. Use /api/projects endpoints for persistence.'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
