# QuickX - Lightweight File Receiver

A simple, toggleable file receiver service with a beautiful web interface. Perfect for quickly receiving files over the internet via Cloudflare tunnels or other reverse proxies.

## Features

- Beautiful, responsive drag-and-drop web interface
- No file size limits
- Toggle on/off with a single command
- Runs on localhost:8080 when enabled
- Automatic duplicate file handling
- Systemd service integration
- Clean, minimal Python Flask backend

## Screenshots

The interface features a modern purple gradient design with:
- Drag & drop file upload
- Multiple file selection
- Upload progress tracking
- Real-time status updates

## Installation

### Prerequisites

- Ubuntu/Debian-based Linux system
- nginx
- Python 3
- sudo access

### Quick Install

```bash
# 1. Install Python dependencies
sudo pip3 install flask flask-cors

# 2. Create directory structure
sudo mkdir -p /var/www/quickx/uploads
sudo chown -R www-data:www-data /var/www/quickx

# 3. Copy files
sudo cp index.html /var/www/quickx/
sudo cp upload_server.py /var/www/quickx/
sudo chmod 755 /var/www/quickx/upload_server.py

# 4. Install nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/quickx

# 5. Install systemd service
sudo cp file-receiver.service /etc/systemd/system/
sudo systemctl daemon-reload

# 6. Install quickx command
sudo cp quickx /usr/local/bin/
sudo chmod +x /usr/local/bin/quickx
```

## Usage

### Start the file receiver
```bash
quickx start
```
The service will be available at `http://localhost:8080`

### Stop the file receiver
```bash
quickx stop
```

### Check status
```bash
quickx status
```

### Restart
```bash
quickx restart
```

## How It Works

1. **Web Interface** (`index.html`) - Beautiful drag-and-drop interface served by nginx
2. **Backend** (`upload_server.py`) - Flask application handling file uploads on port 5000
3. **Nginx** (`nginx.conf`) - Reverse proxy serving the interface on port 8080 and proxying uploads to Flask
4. **Systemd Service** (`file-receiver.service`) - Manages the Flask backend
5. **Control Script** (`quickx`) - Convenient command to start/stop everything

## File Locations

- **Web files**: `/var/www/quickx/`
- **Uploaded files**: `/var/www/quickx/uploads/`
- **nginx config**: `/etc/nginx/sites-available/quickx`
- **Systemd service**: `/etc/systemd/system/file-receiver.service`
- **Control script**: `/usr/local/bin/quickx`

## Configuration

### Change Upload Directory

Edit `/var/www/quickx/upload_server.py`:
```python
UPLOAD_FOLDER = '/your/custom/path'
```

### Change Port

Edit `/etc/nginx/sites-available/quickx`:
```nginx
listen 8080;  # Change to your desired port
```

## Use with Cloudflare Tunnel

1. Start quickx: `quickx start`
2. Create/start your Cloudflare tunnel pointing to `localhost:8080`
3. Share the Cloudflare URL with others
4. When done: `quickx stop`

## Security Notes

- The service only listens on localhost (127.0.0.1)
- Access control should be handled by your reverse proxy (e.g., Cloudflare Access)
- Files are saved with sanitized filenames to prevent directory traversal
- No authentication is built-in - use Cloudflare Access or similar for access control

## Troubleshooting

### Service won't start
```bash
# Check service logs
sudo journalctl -u file-receiver -n 50

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Port already in use
```bash
# Check what's using port 8080
sudo lsof -i :8080

# Or check port 5000 (Flask backend)
sudo lsof -i :5000
```

### Uploads failing
```bash
# Check permissions
ls -la /var/www/quickx/uploads/

# Should show:
# drwxr-xr-x www-data www-data
```

## Uninstall

```bash
# Stop and disable service
quickx stop
sudo systemctl disable file-receiver

# Remove files
sudo rm -rf /var/www/quickx
sudo rm /etc/nginx/sites-available/quickx
sudo rm /etc/systemd/system/file-receiver.service
sudo rm /usr/local/bin/quickx

# Reload services
sudo systemctl daemon-reload
sudo systemctl reload nginx
```

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Pull requests welcome! This is a simple project meant to be easily customizable.
