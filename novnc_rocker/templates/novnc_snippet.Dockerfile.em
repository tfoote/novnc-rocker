RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN \
	apt-get update \
	&& \
	apt-get install --yes \
		net-tools \
        python3-pip \
        git
RUN \
	pip3 install --no-cache-dir \
		numpy \
	&& \
	git clone https://github.com/novnc/noVNC.git /usr/src/app/noVNC \
	&& \
	git clone https://github.com/kanaka/websockify /usr/src/app/noVNC/utils/websockify \
	;
