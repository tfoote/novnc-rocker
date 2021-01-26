RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends \
		net-tools \
		nginx-full \
        python3-pip \
        git\
        supervisor \
	&& rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt
WORKDIR /opt

RUN \
	git clone https://github.com/novnc/noVNC.git /opt/noVNC \
	&& \
	git clone https://github.com/kanaka/websockify /opt/noVNC/utils/websockify \
	;


RUN mkdir -p /root/.supervisor/conf.d

COPY supervisor.conf /root/.supervisor
COPY novnc.conf /root/.supervisor/conf.d
COPY nginx.conf /root/.supervisor/conf.d

COPY self.pem /root/self.pem
COPY .htpasswd /opt/noVNC
COPY rproxy-nginx-site /etc/nginx/sites-available
RUN ln -s /etc/nginx/sites-available/rproxy-nginx-site /etc/nginx/sites-enabled/rproxy-nginx-site