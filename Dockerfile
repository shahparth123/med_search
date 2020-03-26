FROM ubuntu:latest
MAINTAINER parth shah <parth@parthhosting.com>
LABEL Description="This image is med search server"\
        Vendor="Parth Shah"\
        Version="0.1"
RUN apt-get -y update
RUN apt-get -y install python3 python3-dev python3-pip git
RUN pip3 install --upgrade pip
# install Python modules needed by the Python app
COPY search_server.py /search_server.py
COPY requirements.txt /static
COPY templates /templates
COPY static /static
RUN pip3 install --no-cache-dir -r /requirements.txt
# tell the port number the container should expose
EXPOSE 5000
# run the application
CMD ["python3", "/search_server.py"]
#CMD ["/bin/bash"]