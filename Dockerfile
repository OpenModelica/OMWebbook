FROM ubuntu:20.04
MAINTAINER Arunkumar Palanisamy "arunkumar.palanisamy@liu.se"

RUN apt-get update

# Add OpenModelica release build
RUN DEBIAN_FRONTEND=noninteractive apt install -y gnupg lsb-release wget
RUN for deb in deb deb-src; do echo "$deb http://build.openmodelica.org/apt `lsb_release -cs` release"; done | tee /etc/apt/sources.list.d/openmodelica.list
RUN wget -q http://build.openmodelica.org/apt/openmodelica.asc -O- | apt-key add -

# Update index (again)
RUN apt-get update

# install openmodelica
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openmodelica
# install libraries
RUN for PKG in `apt-cache search "omlib-.*" | cut -d" " -f1`; do apt-get install -y "$PKG"; done

# Install Python components
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip python3-dev build-essential

# Install git nginx supervisor
RUN apt-get install -y git nginx supervisor

# always upgrade pip
RUN pip3 install --upgrade pip

# Install OMPython
RUN pip3 install git+git://github.com/OpenModelica/OMPython.git

# Install webdevelopment tools and webservers
RUN pip3 install flask futures gunicorn

#EXPOSE 5000

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy the Project and setup workdir
ADD . /OMWebbook
WORKDIR /OMWebbook

# Start processes
CMD ["supervisord","-c","/etc/supervisor/conf.d/supervisord.conf"]
