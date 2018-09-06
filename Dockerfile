FROM ubuntu:14.04
MAINTAINER Arunkumar Palanisamy "arunkumar.palanisamy@liu.se"

RUN apt-get update 
# Install wget
RUN apt-get install -y wget

# Add OpenModelica stable build
RUN for deb in deb deb-src; do echo "$deb http://build.openmodelica.org/apt `lsb_release -cs` stable"; done | sudo tee /etc/apt/sources.list.d/openmodelica.list
RUN wget -q http://build.openmodelica.org/apt/openmodelica.asc -O- | sudo apt-key add - 

# Update index (again)
RUN apt-get update

# Install OpenModelica
RUN apt-get install -y openmodelica

RUN apt-get install -y python-pip python-dev build-essential 
RUN apt-get install -y omniidl \
                       omniidl-python \
                       omniorb \
                       omniorb-idl \
	                   git \
					   python-numpy \
                       nginx \
                       supervisor \
                       python-omniorb 

# Install OMPython                        
RUN sudo pip install git+https://github.com/arun3688/OMPython

# Install webdevelopment tools and webservers
RUN pip install flask futures gunicorn

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
