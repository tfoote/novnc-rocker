ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.2.5
ARG VIRTUALGL_VERSION=2.6.5

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends \
        ca-certificates \
        curl \
    	lubuntu-desktop \
        mesa-utils \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    curl -fsSL -O ${SOURCEFORGE}/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
    && dpkg -i *.deb \
    && rm -f /tmp/*.deb \
    && sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver

RUN mkdir -p /root/.vnc
RUN echo testpass | /opt/TurboVNC/bin/vncpasswd -f > /root/.vnc/passwd && chmod 600 /root/.vnc/passwd

RUN mkdir -p /root/.supervisor/conf.d

COPY supervisor.conf /root/.supervisor
COPY turbovnc.conf /root/.supervisor/conf.d

CMD /usr/bin/supervisord -c /root/.supervisor/supervisor.conf