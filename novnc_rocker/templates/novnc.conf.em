[program:novnc]
command=/opt/noVNC/utils/novnc_proxy --vnc localhost:5901 --listen @(novnc_port - 2000)
# --cert /root/self.pem --ssl-only
autorestart=true