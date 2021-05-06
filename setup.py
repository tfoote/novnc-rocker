import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="novnc-rocker",
    version="0.0.1",
    packages=setuptools.find_packages(),
    package_data={'novnc_rocker': ['templates/*.em',
        'templates/self.pem',
        'templates/nginx.conf',
        'templates/supervisor.conf',
        'templates/turbovnc.conf',
        'templates/.htpasswd']},
    author="Tully Foote",
    author_email="tfoote@osrfoundation.org",
    description="Plugins for rocker that inject noVNC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tfoote/novnc-rocker",
    license='Apache 2.0',
    install_requires=[
        'rocker',
    ],
    entry_points={
        'rocker.extensions': [
            'fuse = novnc_rocker.fuse:Fuse',
            'novnc = novnc_rocker.novnc:NoVNC',
            'turbovnc = novnc_rocker.turbovnc:TurboVNC',
        ]
    }
)