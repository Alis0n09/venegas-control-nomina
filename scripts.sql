CREATE USER venegas_nominas_user WITH PASSWORD 'venegas_nominas_pass';
CREATE DATABASE venegas_nominas_db OWNER venegas_nominas_user;
GRANT ALL PRIVILEGES ON DATABASE venegas_nominas_db TO venegas_nominas_user;

ALTER USER venegas_nominas_user7 CREATEDB;


sudo chown -R root:root /opt/venegas-control-nomina/staticfiles
sudo chmod -R 755 /opt/venegas-control-nomina/staticfiles
sudo chmod -R 755 /opt/venegas-control-nomina




[Unit]
Description=Gunicorn daemon for venegas-control-nomina
After=network.target postgresql.service

[Service]
User=root
Group=root
WorkingDirectory=/opt/venegas-control-nomina
Environment="PATH=/opt/venegas-control-nomina/.venv/bin"
EnvironmentFile=/opt/venegas-control-nomina/.env
ExecStart=/opt/venegas-control-nomina/.venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/run/gunicorn-venegas-control-nomina.sock \
          --access-logfile /var/log/gunicorn-venegas-control-nomina-access.log \
          --error-logfile /var/log/gunicorn-venegas-control-nomina-error.log \
          config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target



sudo touch /var/log/gunicorn-venegas-control-nomina-access.log
sudo touch /var/log/gunicorn-venegas-control-nomina-error.log
sudo chown root:root /var/log/gunicorn-venegas-control-nomina-*.log



sudo systemctl daemon-reload
sudo systemctl start gunicorn-venegas-control-nomina
sudo systemctl enable gunicorn-venegas-control-nomina
sudo systemctl status gunicorn-venegas-control-nomina




certbot --nginx -d venegas-nominas.uaeftt-ute.site

server {
    listen 80;
    server_name venegas-nominas.uaeftt-ute.site;

    # Logs
    access_log /var/log/nginx/venegas-control-nomina-access.log;
    error_log  /var/log/nginx/venegas-control-nomina-error.log;

    # Archivos estáticos (incluye CSS del admin de Django)
    location /static/ {
        alias /opt/venegas-control-nomina/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Peticiones a la API via Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn-venegas-control-nomina.sock;
        proxy_read_timeout 90;
        proxy_connect_timeout 90;
    }
}


sudo ln -s /etc/nginx/sites-available/venegas-control-nomina /etc/nginx/sites-enabled/