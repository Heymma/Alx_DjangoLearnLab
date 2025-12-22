# Deployment Configuration for HTTPS (Step 4)

## Overview
To enforce HTTPS, configure your web server (e.g., Nginx or Apache) to handle SSL/TLS certificates and redirect HTTP to HTTPS. Use free certificates from Let's Encrypt or a provider like Certbot. Below is a sample Nginx configuration. Update your server's config file (e.g., /etc/nginx/sites-available/default) and restart the server.

## Sample Nginx Configuration
server {
    listen 80 default_server;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;  # Redirect all HTTP to HTTPS
}

server {
    listen 443 ssl default_server;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;  # Path to your SSL certificate
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;  # Path to your private key

    # Additional security headers (complements Django settings)
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Proxy to your Django server (e.g., gunicorn or uWSGI)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/static/files/;  # Serve static files
    }
}

## Steps to Set Up
1. Install Certbot: sudo apt install certbot python3-certbot-nginx (on Ubuntu).
2. Obtain certificate: sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com.
3. Restart Nginx: sudo systemctl restart nginx.
4. Test: Visit http://yourdomain.com - it should redirect to HTTPS, and check headers with browser dev tools or curl -I https://yourdomain.com.

## For Apache (Alternative)
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

    # Headers
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

    # Proxy to Django
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>