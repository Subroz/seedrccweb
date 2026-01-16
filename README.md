# ⚡ CloudTorrent - Seedr Web Interface

> A beautiful, feature-rich web interface for [Seedr.cc](https://www.seedr.cc/) cloud torrent service. Built with Flask and a stunning cyberpunk-inspired UI with dual access modes for public sharing and private management.

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-00f5d4?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.8+-7b2cbf?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0+-ff006e?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-f39c12?style=for-the-badge" alt="License">
</p>

---

## 🌟 Overview

CloudTorrent provides a modern, intuitive web interface to interact with your Seedr.cc cloud storage. It features two distinct operational modes:

- **🌐 Public Mode** - Share your Seedr files with anyone via a web interface (read-only access with torrent adding)
- **🔐 Owner Mode** - Full administrative control with authentication for managing your account

### Why CloudTorrent?

- **Beautiful UI**: Cyberpunk-inspired design with Aurora animations and responsive layout
- **Dual Access Modes**: Public file sharing + secure owner management
- **Real-time Updates**: Live download progress tracking with auto-refresh
- **Video Streaming**: Built-in video player for supported formats
- **Smart Storage Alerts**: Automatic warnings when storage is running low
- **Zero Configuration**: Auto-saves token on owner login for instant public access

---

## ✨ Features

### 🌐 Public Access Features
- 📁 **File Browser** - Navigate through shared Seedr folders
- ⬇️ **Direct Downloads** - Get direct download links for any file
- 🎬 **Video Streaming** - Stream MP4, WebM, and other supported formats in-browser
- 🧲 **Add Torrents** - Add magnet links or torrent URLs (if enabled)
- 📊 **Storage Monitor** - Real-time storage usage visualization
- ⏱️ **Download Progress** - Live tracking of active torrent downloads
- 🎨 **Beautiful UI** - Aurora-animated background with modern cyberpunk aesthetics
- 📱 **Responsive Design** - Optimized for desktop, tablet, and mobile devices

### 🔐 Owner Mode Features
- 🔑 **Secure Login** - Authenticate with Seedr email/password
- 💾 **Auto Token Save** - Automatically saves access token to `config.json`
- 🗑️ **File Management** - Delete files and folders directly from the interface
- 🧲 **Torrent Management** - Full control over adding torrents
- 🔄 **Session Management** - Secure owner sessions with logout functionality
- 🎯 **Token Extraction** - View and manage access tokens

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed on your system
- A **[Seedr.cc](https://www.seedr.cc/)** account (free or premium)

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Subroz/seedrccweb.git
cd seedrccweb
```

#### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install flask flask-cors seedr
```

#### 3️⃣ Configure (Optional)

You can enable public access by either:

**Option A: Using config.json (Recommended)**
```json
{
    "seedr_token": "your-access-token-here"
}
```

**Option B: Using Environment Variable**
```bash
export SEEDR_TOKEN="your-access-token-here"
```

> **Note:** You don't need to configure manually. Just login via the owner panel, and the token will be auto-saved!

#### 4️⃣ Run the Application

```bash
python app.py
```

#### 5️⃣ Access the Interface

- **Public Interface**: `http://localhost:5000`
- **Owner Panel**: `http://localhost:5000/owner-login`

---

## 📖 Usage Guide

### 🌐 Public Mode (File Sharing)

1. Navigate to `http://localhost:5000`
2. Browse files and folders
3. Click on files to download
4. Use the ▶️ button to stream videos
5. Add torrents using the magnet link input (if enabled)

**Note:** Public mode requires a valid token to be configured (automatically done after owner login).

### 🔐 Owner Mode (Administration)

#### First Time Setup

1. Navigate to `http://localhost:5000/owner-login`
2. Enter your Seedr.cc email and password
3. Click "Sign In"
4. ✅ Token is **automatically saved** to `config.json`
5. 🎉 Public access is now enabled!

#### Managing Files

- **View Files**: Browse all your Seedr files and folders
- **Delete Items**: Use delete buttons on files/folders (owner mode only)
- **Add Torrents**: Add magnet links or torrent URLs
- **Monitor Storage**: Real-time storage usage with warnings

#### API Access

Owner mode provides secure API endpoints:

```javascript
// Example: Add a torrent (requires owner session)
fetch('/api/owner/torrent', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Session-ID': 'your-session-id'
    },
    body: JSON.stringify({ link: 'magnet:?xt=...' })
});
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SEEDR_TOKEN` | Seedr access token for public mode | None |
| `FLASK_DEBUG` | Enable Flask debug mode | `False` |
| `FLASK_RUN_PORT` | Port to run the server on | `5000` |

### Configuration File (`config.json`)

```json
{
    "seedr_token": "your-seedr-access-token-here"
}
```

The token is automatically saved when you login through the owner panel.

### Running on a Custom Port

```bash
python app.py  # Runs on port 5000 by default
```

To change the port, modify the `app.run()` line in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 🐳 Docker Deployment

### Using Docker

#### 1️⃣ Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

#### 2️⃣ Build and Run

```bash
# Build the image
docker build -t cloudtorrent .

# Run the container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/config.json:/app/config.json \
  --name cloudtorrent \
  cloudtorrent
```

#### 3️⃣ With Environment Variables

```bash
docker run -d \
  -p 5000:5000 \
  -e SEEDR_TOKEN="your-token-here" \
  --name cloudtorrent \
  cloudtorrent
```

### Using Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  cloudtorrent:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./config.json:/app/config.json
    environment:
      - SEEDR_TOKEN=${SEEDR_TOKEN}
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

---

## 🚀 Production Deployment

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Gunicorn + Nginx

#### 1️⃣ Gunicorn Configuration (`gunicorn_config.py`)

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
```

#### 2️⃣ Run Gunicorn

```bash
gunicorn -c gunicorn_config.py app:app
```

#### 3️⃣ Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Using systemd (Linux Service)

Create `/etc/systemd/system/cloudtorrent.service`:

```ini
[Unit]
Description=CloudTorrent Seedr Web Interface
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/seedrccweb
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable cloudtorrent
sudo systemctl start cloudtorrent
sudo systemctl status cloudtorrent
```

---

## 📁 Project Structure

```
seedrccweb/
├── app.py                 # Flask backend application with dual-mode API
├── index.html            # Public interface (beautiful file browser)
├── owner.html            # Owner login and management interface
├── requirements.txt      # Python package dependencies
├── config.json           # Configuration file (auto-generated)
├── LICENSE               # MIT License
└── README.md             # This documentation
```

### Key Files

- **`app.py`**: Main Flask application with public and owner API routes
- **`index.html`**: Public-facing interface with file browsing and streaming
- **`owner.html`**: Administrative interface for owner authentication
- **`config.json`**: Auto-generated configuration with saved token

---

## 🔌 API Documentation

### Public Endpoints

#### `GET /api/status`
Check API status and public access availability.

**Response:**
```json
{
    "status": "online",
    "seedr_available": true,
    "public_access": true,
    "message": "Public access ready"
}
```

#### `GET /api/drive`
Get root folder contents and storage information.

**Response:**
```json
{
    "space_used": 1073741824,
    "space_max": 10737418240,
    "folders": [...],
    "files": [...],
    "torrents": [...]
}
```

#### `GET /api/folder/<folder_id>`
Get contents of a specific folder.

#### `GET /api/file/<file_id>`
Get file information including download URL.

#### `POST /api/torrent`
Add a torrent (public mode).

**Request:**
```json
{
    "link": "magnet:?xt=urn:btih:..."
}
```

### Owner Endpoints (Require Authentication)

#### `POST /api/owner/login`
Authenticate as owner with Seedr credentials.

**Request:**
```json
{
    "email": "your@email.com",
    "password": "your-password"
}
```

**Response:**
```json
{
    "success": true,
    "session_id": "abc123...",
    "token_saved": true,
    "space_used": 1073741824,
    "space_max": 10737418240
}
```

#### `POST /api/owner/logout`
Logout from owner session.

#### `DELETE /api/owner/file/<file_id>`
Delete a file (owner only).

#### `DELETE /api/owner/folder/<folder_id>`
Delete a folder (owner only).

---

## 🛡️ Security Considerations

### Best Practices

- ✅ **Use HTTPS** in production to encrypt token transmission
- ✅ **Restrict Access** to owner panel using firewall rules or authentication proxy
- ✅ **Regular Backups** of `config.json` containing your token
- ✅ **Environment Variables** for sensitive data in production
- ✅ **Secure Sessions** - Sessions are stored in memory (consider Redis for production)

### Token Security

- 🔐 Tokens are stored in `config.json` with restricted file permissions
- 🔐 Never commit `config.json` to version control (already in `.gitignore`)
- 🔐 Owner sessions use cryptographically secure session IDs
- 🔐 Credentials are never stored on the server

### Production Recommendations

1. **Use a reverse proxy** (Nginx/Apache) with HTTPS
2. **Configure firewall** to restrict owner panel access
3. **Enable rate limiting** to prevent abuse
4. **Monitor logs** for suspicious activity
5. **Use Redis** for session storage in production

---

## 🐛 Troubleshooting

### "Seedr package not installed"

```bash
pip install seedr
# or
pip install -r requirements.txt
```

### "Public access not configured"

**Solution:** Login via the owner panel at `/owner-login`. The token will be auto-saved.

### "Invalid login credentials"

- ✅ Verify your email and password are correct
- ✅ Check your Seedr.cc account status
- ✅ Ensure your account has verified email

### "Connection refused" / Port Already in Use

```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill the process using the port
kill -9 <PID>

# Or run on a different port
python app.py  # Edit app.py to change port
```

### Files Not Showing / Empty State

- 🔄 Click the "Refresh" button
- 🔄 Check your Seedr.cc account directly
- 🔄 Verify the token is valid and not expired
- 🔄 Check browser console for JavaScript errors

### Video Streaming Not Working

- ✅ Ensure the file format is supported (MP4, WebM, MOV, M4V)
- ✅ Check that the file has finished downloading in Seedr
- ✅ Verify your browser supports HTML5 video
- ✅ Try downloading the file instead of streaming

### Storage Warning Shows Incorrect Data

- 🔄 Refresh the page to update storage information
- 🔄 Login to Seedr.cc directly to verify storage usage
- 🔄 Delete some files to free up space

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Subroz/seedrccweb.git
cd seedrccweb

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in debug mode
export FLASK_DEBUG=1
python app.py
```

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 CloudTorrent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Credits & Acknowledgments

- **[Seedr.cc](https://www.seedr.cc/)** - Excellent cloud torrent service
- **[seedrcc Python Library](https://github.com/hemantapkh/seedrcc)** - Python wrapper for Seedr API
- **[Flask](https://flask.palletsprojects.com/)** - Web framework
- **[Font Awesome](https://fontawesome.com/)** - Icons (via emoji alternatives)

---

## 📞 Support

If you encounter any issues or have questions:

1. **Check the Troubleshooting section** above
2. **Search existing issues** on [GitHub Issues](https://github.com/Subroz/seedrccweb/issues)
3. **Create a new issue** with detailed information about your problem

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub! ⭐

---

<p align="center">
  <strong>Made with ❤️ by Subro</strong><br>
  <sub>Powered by Flask • Seedr.cc • Python</sub>
</p>
