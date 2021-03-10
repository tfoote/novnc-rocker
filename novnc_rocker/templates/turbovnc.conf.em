[program:turbovnc]
command=/opt/TurboVNC/bin/vncserver  -SecurityTypes None -fg -nohttpd -geometry 1280x720
autorestart=true
user=@(vnc_user)
environment=USER="@(vnc_user)",HOME="@(vnc_user_home)",TVNC_WM="lxqt-session"