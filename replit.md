# CloudTorrent - Seedr Web Interface

## Overview

CloudTorrent is a Flask-based web application that provides a modern, cyberpunk-styled interface for interacting with the Seedr.cc cloud torrent service. The application supports two operational modes:

- **Public Mode**: Allows anyone to browse and download shared files, stream videos, and optionally add torrents
- **Owner Mode**: Provides authenticated access for full account management including file deletion and token management

The application wraps the Seedr API through the `seedr` Python package and presents it through a responsive web interface with real-time download progress tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

**Backend Framework**: Flask with Flask-CORS for cross-origin support
- Single `app.py` file handles all backend logic
- Configuration stored in `config.json` for persistence
- Session-based authentication using Flask's secret key mechanism

**Frontend Architecture**: Server-side rendered HTML templates
- `index.html` - Public file browser interface
- `owner.html` - Owner authentication/login page
- Templates served directly from the root directory (template_folder='.')
- Styling uses CSS custom properties (variables) for theming
- Google Fonts integration (Sora, DM Sans, JetBrains Mono, Space Mono, Outfit)

**Design Pattern**: Monolithic single-file backend
- All routes, configuration management, and API interactions in one file
- Utility functions for config loading/saving
- Decorator-based authentication pattern (indicated by `@wraps` import)

### Authentication Flow

1. Owner logs in with Seedr email/password through `/owner` route
2. On successful login, access token is automatically saved to `config.json`
3. Public mode reads token from `config.json` for API calls
4. Owner sessions managed through Flask's session mechanism

### Configuration Management

- `config.json` stores persistent settings including `seedr_token`
- Config file is loaded/saved via helper functions
- Located in same directory as `app.py`

## External Dependencies

### Python Packages
- **Flask** (>=2.0.0): Web framework
- **Flask-CORS** (>=3.0.0): Cross-origin resource sharing
- **seedr** (>=1.0.0): Third-party Seedr.cc API wrapper - handles all interactions with Seedr service

### External Services
- **Seedr.cc**: Cloud torrent service that the application interfaces with
- **Google Fonts**: External font loading for UI typography

### API Integration
- The `seedr` package provides `SeedrAPI` class for API calls
- Error handling for `InvalidLogin`, `InvalidToken`, and `LoginRequired` exceptions
- Graceful degradation if seedr package is not installed (SEEDR_AVAILABLE flag)