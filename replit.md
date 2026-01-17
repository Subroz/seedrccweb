# CloudTorrent - Seedr Web Interface

## Overview

CloudTorrent is a Flask-based web application that provides a modern, cyberpunk-themed interface for the Seedr.cc cloud torrent service. The application features two operational modes:

1. **Public Mode** - Allows anyone to browse and download shared files, stream videos, and optionally add torrents
2. **Owner Mode** - Provides authenticated administrative access for full account management including file deletion and token management

The project uses a simple architecture with Flask serving both the API backend and HTML templates directly, with no separate frontend build process.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask** serves as the web framework, handling both API endpoints and template rendering
- Templates (index.html, owner.html) are served directly from the project root rather than a dedicated templates folder
- CORS is enabled via flask-cors for cross-origin requests

### Authentication & Session Management
- Flask sessions with a randomly generated secret key handle owner authentication
- Owner mode requires Seedr email/password login, which then extracts and stores an access token
- The access token is persisted to `config.json` for subsequent public access without re-authentication

### Configuration Storage
- Simple JSON file (`config.json`) stores the Seedr API token
- No database is used - configuration is file-based for simplicity
- The config file is located in the same directory as the application

### External API Integration
- The `seedr` Python package wraps the Seedr.cc API for all torrent and file operations
- The application gracefully handles the case where the seedr package is not installed
- All Seedr operations (file listing, downloads, torrent management) go through this package

### Frontend Architecture
- Static HTML pages with inline CSS and JavaScript (no build tools or bundlers)
- Cyberpunk/Aurora-inspired visual design with CSS custom properties for theming
- Google Fonts integration (Sora, DM Sans, JetBrains Mono, Space Mono, Outfit)
- Responsive design supporting desktop, tablet, and mobile devices

### Key Design Decisions
- **Monolithic structure**: Single app.py file contains all backend logic for simplicity
- **No database**: Token storage uses a JSON file, suitable for single-user deployment
- **Template co-location**: HTML files live in project root, configured via `template_folder='.'`
- **Graceful degradation**: Application runs even if seedr package is missing, with appropriate warnings

## External Dependencies

### Python Packages
- **Flask (>=2.0.0)** - Web framework for routing and template serving
- **flask-cors (>=3.0.0)** - Enables Cross-Origin Resource Sharing
- **seedr (>=1.0.0)** - Python wrapper for the Seedr.cc API (handles authentication, file operations, torrent management)

### External Services
- **Seedr.cc** - Cloud torrent service that the application interfaces with. Requires a Seedr account for functionality
- **Google Fonts CDN** - Provides custom typography (Sora, DM Sans, JetBrains Mono, Space Mono, Outfit font families)

### Configuration Files
- **config.json** - Stores the Seedr API access token. Created/updated when owner logs in successfully