RUN \
	apt-get update \
	&& \
	apt-get install --yes \
		net-tools \
        python3-pip \
        git\
        supervisor 
RUN mkdir -p /opt
WORKDIR /opt

RUN \
	pip3 install --no-cache-dir \
		numpy \
	&& \
	git clone https://github.com/novnc/noVNC.git /opt/noVNC \
	&& \
	git clone https://github.com/kanaka/websockify /opt/noVNC/utils/websockify \
	;


RUN mkdir -p /root/.supervisor/conf.d

COPY supervisor.conf /root/.supervisor
COPY novnc.conf /root/.supervisor/conf.d
