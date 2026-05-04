from flask import Flask, send_file, request, jsonify
from pymongo import MongoClient, ASCENDING, DESCENDING, UpdateOne
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os
import re
import json
import time
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Password (set via environment variable or default)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, 'app.html')
load_dotenv(os.path.join(BASE_DIR, '.env'))

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


def summarize_project_data(data):
    if not isinstance(data, dict):
        return {'valid': False}
    rate_cards = data.get('rateCards') if isinstance(data.get('rateCards'), dict) else {}
    cost_lines = data.get('costLines') if isinstance(data.get('costLines'), list) else []

    nonzero_rates = 0
    for arr in rate_cards.values():
        if not isinstance(arr, list):
            continue
        for rate in arr:
            if not isinstance(rate, dict):
                continue
            try:
                if float(rate.get('value') or 0) != 0:
                    nonzero_rates += 1
            except Exception:
                pass

    nonzero_month_cells = 0
    for line in cost_lines:
        if not isinstance(line, dict):
            continue
        for v in (line.get('monthly') or []):
            try:
                if float(v or 0) != 0:
                    nonzero_month_cells += 1
            except Exception:
                pass

    return {
        'valid': True,
        'projectName': data.get('projectInputs', {}).get('projectName'),
        'nonzeroRates': nonzero_rates,
        'nonzeroMonthlyCells': nonzero_month_cells,
        'costLines': len(cost_lines),
    }


@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_file(HTML_FILE)


@app.route('/api/projects', methods=['GET'])
def list_projects():
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    docs = list(projects_col.find({}, {'data': 0}).sort('updatedAt', DESCENDING))
    app.logger.info("GET /api/projects -> %s projects", len(docs))
    return jsonify({'success': True, 'projects': [serialize_project_meta(d) for d in docs]})


@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    pid = clean_project_id(project_id)
    doc = projects_col.find_one({'_id': pid})
    if not doc:
        return jsonify({'success': False, 'error': 'Project not found'}), 404

    app.logger.info("GET /api/projects/%s -> found=%s", pid, bool(doc))
    return jsonify({'success': True, 'project': serialize_project_full(doc)})


@app.route('/api/projects', methods=['POST'])
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

    app.logger.info("POST /api/projects -> created id=%s name=%s summary=%s", pid, cleaned['name'], summarize_project_data(cleaned['data']))
    return jsonify({'success': True, 'project': serialize_project_full(doc)}), 201


@app.route('/api/projects/<project_id>', methods=['PUT'])
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
    before = projects_col.find_one({'_id': pid}, {'name': 1, 'updatedAt': 1})
    summary = summarize_project_data(cleaned['data']) if cleaned['data'] is not None else {'valid': False, 'note': 'no data payload'}

    result = projects_col.update_one({'_id': pid}, {'$set': update})
    if result.matched_count == 0:
        return jsonify({'success': False, 'error': 'Project not found'}), 404

    doc = projects_col.find_one({'_id': pid})
    app.logger.info(
        "PUT /api/projects/%s -> matched=%s modified=%s beforeUpdatedAt=%s afterUpdatedAt=%s name=%s payloadSummary=%s",
        pid,
        result.matched_count,
        result.modified_count,
        before.get('updatedAt') if before else None,
        doc.get('updatedAt') if doc else None,
        update.get('name'),
        summary
    )
    return jsonify({'success': True, 'project': serialize_project_full(doc)})


@app.route('/api/projects/<project_id>', methods=['DELETE'])
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

    app.logger.info("DELETE /api/projects/%s -> deleted=%s", pid, result.deleted_count)
    return jsonify({'success': True})


@app.route('/api/projects/export', methods=['GET'])
def export_projects():
    ready, error = ensure_db_ready()
    if not ready:
        return jsonify({'success': False, 'error': error}), 503

    docs = list(projects_col.find({}).sort('updatedAt', DESCENDING))
    app.logger.info("GET /api/projects/export -> %s projects", len(docs))
    return jsonify({'success': True, 'projects': [serialize_project_full(d) for d in docs]})


@app.route('/api/projects/import', methods=['POST'])
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

    app.logger.info("POST /api/projects/import -> imported=%s mode=%s", imported, mode)
    return jsonify({'success': True, 'imported': imported, 'mode': mode})


@app.route('/api/save', methods=['POST'])
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
