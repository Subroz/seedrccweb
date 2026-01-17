# CloudTorrent - Seedr Cloud Downloader

## Overview
A web application that allows users to download files via Seedr.cc. Features public access mode for browsing/downloading and owner authentication for token management.

## Project Structure
- `app.py` - Flask backend with API routes for Seedr integration
- `index.html` - Public user interface for browsing and downloading
- `owner.html` - Owner login page for token management
- `config.json` - Configuration file (auto-created) storing the Seedr token
- `requirements.txt` - Python dependencies

## Running the Application
The Flask server runs on port 5000:
```
python app.py
```

## Configuration
- **SEEDR_TOKEN**: Environment variable for Seedr API access token
- Alternatively, the owner can log in at `/owner-login` to auto-save the token to `config.json`

## Dependencies
- Flask >= 2.0.0
- Flask-CORS >= 3.0.0  
- Seedr >= 1.0.0

## API Endpoints

### Public Routes
- `GET /` - Main public page
- `GET /api/status` - Check API status
- `GET /api/drive` - Get drive information
- `GET /api/folder/<id>` - Get folder contents
- `GET /api/file/<id>` - Get file info and download link
- `POST /api/torrent` - Add torrent/magnet link

### Owner Routes
- `GET /owner-login` - Owner login page
- `POST /api/owner/login` - Authenticate owner
- `POST /api/owner/logout` - Logout owner
- `GET /api/owner/token` - Get access token
- `POST /api/owner/save-token` - Save token to config
