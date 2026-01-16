# ⚡ CloudTorrent - Seedr Cloud Downloader

A beautiful, modern web interface for downloading files via Seedr.cc. Built with Flask and a stunning cyberpunk-inspired UI.

![CloudTorrent Preview](https://img.shields.io/badge/Status-Ready-00f5d4?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-7b2cbf?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-ff006e?style=for-the-badge&logo=flask)

## ✨ Features

- 🔐 **Secure Authentication** - Login with email/password or access token
- 📁 **File Browser** - Navigate through your Seedr folders
- 🧲 **Magnet Support** - Add torrents via magnet links or .torrent URLs
- ⬇️ **Direct Downloads** - Get direct download links for your files
- 📊 **Storage Monitor** - Track your Seedr storage usage
- 🎨 **Modern UI** - Beautiful cyberpunk-inspired dark theme
- 📱 **Responsive** - Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A [Seedr.cc](https://www.seedr.cc/) account

### Installation

1. **Clone or download this repository**

```bash
git clone <your-repo>
cd seedr-downloader
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask flask-cors seedr
```

3. **Run the application**

```bash
python app.py
```

4. **Open your browser**

Navigate to: `http://localhost:5000`

## 📖 Usage

### Login Methods

**Email & Password:**
1. Enter your Seedr account email
2. Enter your password
3. Click "Sign In"

**Access Token:**
1. If you have an access token, paste it in the token field
2. Click "Connect with Token"

### Adding Torrents

1. Paste a magnet link or torrent URL in the input field
2. Click "Add" or press Enter
3. Watch the download progress

### Downloading Files

1. Navigate through folders by clicking on them
2. Click the download button (⬇️) on any file
3. A new tab will open with the direct download link

### Managing Files

- **Delete**: Click the trash icon (🗑️) on any file or folder
- **Refresh**: Click the refresh button to update the file list
- **Navigate**: Use the breadcrumb to go back to parent folders

## 🔧 Configuration

### Environment Variables (Optional)

```bash
# Change the port
export FLASK_RUN_PORT=8000

# Enable debug mode
export FLASK_DEBUG=1
```

### Running in Production

For production deployment, use a proper WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐳 Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t cloudtorrent .
docker run -p 5000:5000 cloudtorrent
```

## 📁 Project Structure

```
seedr-downloader/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── templates/
    └── index.html      # Frontend UI
```

## 🛡️ Security Notes

- Sessions are stored in memory (use Redis for production)
- Credentials are never stored on the server
- HTTPS is recommended for production deployment

## 🤝 Credits


- [seedrcc](https://github.com/hemantapkh/seedrcc) - Alternative comprehensive wrapper
- [Seedr.cc](https://www.seedr.cc/) - Cloud torrent service

## 📜 License

MIT License - Feel free to use and modify!

## 🐛 Troubleshooting

### "Seedr package not installed"

Run: `pip install seedr`

### "Invalid login credentials"

- Double-check your email and password
- Make sure your Seedr account is active

### "Connection refused"

- Ensure the Flask server is running
- Check if port 5000 is available

### Files not showing

- Click the refresh button
- Check your Seedr account directly

---

Made with ❤️ and ⚡
