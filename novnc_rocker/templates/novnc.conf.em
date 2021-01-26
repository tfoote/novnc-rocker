[program:novnc]
command=/opt/noVNC/utils/launch.sh --vnc localhost:5901 --listen @(novnc_port - 2000)
# --cert /root/self.pem --ssl-only
autorestart=true