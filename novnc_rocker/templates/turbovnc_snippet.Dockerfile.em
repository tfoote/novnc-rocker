ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.2.5
ARG VIRTUALGL_VERSION=2.6.5

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends \
        ca-certificates \
        curl \
    	lubuntu-desktop \
        mesa-utils \
        supervisor \
        xauth \
    && rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    curl -fsSL -O ${SOURCEFORGE}/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
    && dpkg -i *.deb \
    && rm -f /tmp/*.deb

# Keep vnc content out of
RUN echo '$vncUserDir = "/tmp/@(vnc_user)-vnc";' >> /etc/turbovncserver.conf

# TODO(tfoote) authentication
# RUN echo testpass | /opt/TurboVNC/bin/vncpasswd -f > ~/@(vnc_user)-vnc/passwd && chmod -R 600 ~/@(vnc_user)-vnc/passwd
# TODO(tfoote) needed maybe too? && chown -R @(vnc_user) /tmp/@(vnc_user)-vnc/passwd

# Avoid a warning about needing to be owned by root
RUN mkdir -p /tmp/.X11-unix && chmod 0777 /tmp/.X11-unix

RUN mkdir -p /root/.supervisor/conf.d

COPY supervisor.conf /root/.supervisor
COPY turbovnc.conf /root/.supervisor/conf.d


CMD @(vnc_user != 'root' ? 'sudo ' ! '')@ /usr/bin/supervisord -c /root/.supervisor/supervisor.conf