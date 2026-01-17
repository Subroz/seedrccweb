"""
Seedr Cloud Downloader - Flask Backend
A web application that allows users to download files via Seedr.cc
Public access mode with owner authentication for token management.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from functools import wraps
import os
import json
import secrets

app = Flask(__name__, template_folder='.')
app.secret_key = secrets.token_hex(32)
CORS(app)

# Config file path
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

# Try to import seedr - user needs to install it
try:
    from seedr import SeedrAPI
    from seedr.errors import InvalidLogin, InvalidToken, LoginRequired
    SEEDR_AVAILABLE = True
except ImportError:
    SEEDR_AVAILABLE = False
    print("Warning: seedr package not installed. Run: pip install seedr")


def load_config():
    """Load configuration from config.json"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
    return {}


def save_config(config):
    """Save configuration to config.json"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


# Load credentials from environment variables
SEEDR_EMAIL = os.environ.get('SEEDR_EMAIL', '')
SEEDR_PASSWORD = os.environ.get('SEEDR_PASSWORD', '')

# Load token from config file first, then fall back to environment variable
config = load_config()
PUBLIC_TOKEN = config.get('seedr_token', '') or os.environ.get('SEEDR_TOKEN', '')
public_seedr = None

# Owner sessions for token management
owner_sessions = {}


def login_with_credentials():
    """Login using environment credentials and return a SeedrAPI instance"""
    global public_seedr, PUBLIC_TOKEN
    if not SEEDR_AVAILABLE:
        print("Seedr package not available")
        return False
    if not SEEDR_EMAIL or not SEEDR_PASSWORD:
        print("No Seedr credentials configured")
        return False
    try:
        seedr = SeedrAPI(email=SEEDR_EMAIL, password=SEEDR_PASSWORD)
        seedr.get_drive()
        public_seedr = seedr
        token = getattr(seedr, 'access_token', None)
        if token:
            PUBLIC_TOKEN = token
            config = load_config()
            config['seedr_token'] = token
            save_config(config)
        print("Logged in with credentials successfully")
        return True
    except InvalidLogin:
        print("Invalid Seedr credentials")
        return False
    except Exception as e:
        print(f"Failed to login with credentials: {e}")
        return False


def init_public_client():
    """Initialize the public Seedr client - try credentials first, then token"""
    global public_seedr
    if not SEEDR_AVAILABLE:
        return False
    if SEEDR_EMAIL and SEEDR_PASSWORD:
        if login_with_credentials():
            return True
    if PUBLIC_TOKEN:
        try:
            public_seedr = SeedrAPI(token=PUBLIC_TOKEN)
            print("Public Seedr client initialized with token")
            return True
        except Exception as e:
            print(f"Token invalid, trying credentials: {e}")
            if SEEDR_EMAIL and SEEDR_PASSWORD:
                return login_with_credentials()
            return False
    return False


def get_public_client():
    """Get the public Seedr client, re-login if needed"""
    global public_seedr
    if public_seedr is None:
        init_public_client()
    return public_seedr


def require_owner_auth(f):
    """Decorator to require owner authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.headers.get('X-Session-ID') or session.get('owner_session_id')
        if not session_id or session_id not in owner_sessions:
            return jsonify({'error': 'Owner authentication required', 'code': 'AUTH_REQUIRED'}), 401
        return f(*args, **kwargs)
    return decorated


def get_owner_client():
    """Get the Seedr client for the owner session"""
    session_id = request.headers.get('X-Session-ID') or session.get('owner_session_id')
    if session_id and session_id in owner_sessions:
        return owner_sessions[session_id]
    return None


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Serve the main public page"""
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def api_status():
    """Check API status and seedr availability"""
    client = get_public_client()
    return jsonify({
        'status': 'online',
        'seedr_available': SEEDR_AVAILABLE,
        'public_access': client is not None,
        'message': 'Public access ready' if client else 'No public token configured'
    })


@app.route('/api/drive', methods=['GET'])
def get_drive():
    """Get drive information and root folder contents (PUBLIC)"""
    seedr = get_public_client()
    if not seedr:
        return jsonify({'error': 'Public access not configured'}), 503
    try:
        drive_info = seedr.get_drive()
        return jsonify(drive_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/folder/<folder_id>', methods=['GET'])
def get_folder(folder_id):
    """Get contents of a specific folder (PUBLIC)"""
    seedr = get_public_client()
    if not seedr:
        return jsonify({'error': 'Public access not configured'}), 503
    try:
        folder_contents = seedr.get_folder(folder_id)
        return jsonify(folder_contents)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/file/<file_id>', methods=['GET'])
def get_file(file_id):
    """Get file information including download link (PUBLIC)"""
    seedr = get_public_client()
    if not seedr:
        return jsonify({'error': 'Public access not configured'}), 503
    try:
        file_info = seedr.get_file(file_id)
        return jsonify(file_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/torrent', methods=['POST'])
def add_torrent():
    """Add a torrent/magnet link (PUBLIC)"""
    seedr = get_public_client()
    if not seedr:
        return jsonify({'error': 'Public access not configured'}), 503
    
    data = request.get_json()
    link = data.get('link')
    
    if not link:
        return jsonify({'error': 'Torrent link required'}), 400
    
    try:
        result = seedr.add_torrent(link)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== OWNER ROUTES ====================

@app.route('/owner-login')
def owner_login_page():
    """Serve the owner login page"""
    return render_template('owner.html')


@app.route('/api/owner/login', methods=['POST'])
def owner_login():
    """Authenticate owner with Seedr and auto-save token"""
    global PUBLIC_TOKEN, public_seedr
    
    if not SEEDR_AVAILABLE:
        return jsonify({
            'error': 'Seedr package not installed',
            'code': 'SEEDR_NOT_INSTALLED'
        }), 503
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    try:
        seedr = SeedrAPI(email=email, password=password)
        drive_info = seedr.get_drive()
        
        # Create owner session
        session_id = secrets.token_hex(32)
        owner_sessions[session_id] = seedr
        session['owner_session_id'] = session_id
        
        # Auto-save token to config and enable public access
        token = getattr(seedr, 'access_token', None)
        if token:
            config = load_config()
            config['seedr_token'] = token
            save_config(config)
            PUBLIC_TOKEN = token
            public_seedr = seedr
            print("Token auto-saved to config.json - Public access enabled")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'token_saved': bool(token),
            'space_used': drive_info.get('space_used', 0),
            'space_max': drive_info.get('space_max', 0)
        })
        
    except InvalidLogin:
        return jsonify({'error': 'Invalid email or password', 'code': 'INVALID_LOGIN'}), 401
    except Exception as e:
        return jsonify({'error': str(e), 'code': 'UNKNOWN_ERROR'}), 500


@app.route('/api/owner/logout', methods=['POST'])
@require_owner_auth
def owner_logout():
    """Logout owner session"""
    session_id = request.headers.get('X-Session-ID') or session.get('owner_session_id')
    if session_id in owner_sessions:
        del owner_sessions[session_id]
    session.pop('owner_session_id', None)
    return jsonify({'success': True})


@app.route('/api/owner/token', methods=['GET'])
@require_owner_auth
def owner_get_token():
    """Get the access token for the owner session"""
    seedr = get_owner_client()
    try:
        token = getattr(seedr, 'access_token', None)
        if token:
            return jsonify({'token': token})
        return jsonify({'error': 'Token not available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/owner/save-token', methods=['POST'])
@require_owner_auth
def owner_save_token():
    """Save the access token to config file for public access"""
    global PUBLIC_TOKEN, public_seedr
    
    seedr = get_owner_client()
    try:
        token = getattr(seedr, 'access_token', None)
        if not token:
            return jsonify({'error': 'Token not available'}), 404
        
        # Save to config file
        config = load_config()
        config['seedr_token'] = token
        
        if save_config(config):
            # Update the running instance
            PUBLIC_TOKEN = token
            public_seedr = seedr
            return jsonify({'success': True, 'message': 'Token saved to config.json'})
        else:
            return jsonify({'error': 'Failed to save config file'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/owner/torrent', methods=['POST'])
@require_owner_auth
def owner_add_torrent():
    """Add a torrent/magnet link (owner only)"""
    seedr = get_owner_client()
    data = request.get_json()
    link = data.get('link')
    
    if not link:
        return jsonify({'error': 'Torrent link required'}), 400
    
    try:
        result = seedr.add_torrent(link)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/owner/folder/<folder_id>', methods=['DELETE'])
@require_owner_auth
def owner_delete_folder(folder_id):
    """Delete a folder (owner only)"""
    seedr = get_owner_client()
    try:
        seedr.delete_folder(folder_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/owner/file/<file_id>', methods=['DELETE'])
@require_owner_auth
def owner_delete_file(file_id):
    """Delete a file (owner only)"""
    seedr = get_owner_client()
    try:
        seedr.delete_file(file_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n  CloudTorrent - Public Access Mode")
    print("  ==================================")
    if init_public_client():
        print("  Public access: ENABLED")
    elif SEEDR_EMAIL and SEEDR_PASSWORD:
        print("  Public access: FAILED (check credentials)")
    elif PUBLIC_TOKEN:
        print("  Public access: FAILED (invalid token)")
    else:
        print("  Public access: DISABLED (no credentials or token set)")
    print("\n  Public:  http://localhost:5000")
    print("  Owner:   http://localhost:5000/owner-login\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
