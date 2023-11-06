FROM --platform=linux/amd64 ubuntu:16.04
USER root

# Make sure system is up to date
RUN apt-get update -y && apt-get upgrade -y

# Install git (for handwriting repo) and curl (for pip)
RUN apt-get install git -y
RUN apt-get install curl -y0
# Make sure all are up to date
RUN apt-get update -y

# Install python 3.5.2 (default for Ubuntu 16.04)
RUN apt-get install python3 -y
# Confirm python is installed
RUN python3 -V

# Make sure everything is up to date
RUN apt-get update -y && apt-get upgrade -y

# Download and install pip for python 3.5
RUN curl "https://bootstrap.pypa.io/pip/3.5/get-pip.py" -o "get-pip.py"
RUN python3 get-pip.py

# Get handwriting synthesis repo
WORKDIR /root
RUN git clone https://github.com/sjvasquez/handwriting-synthesis
# Install repo dependencies
WORKDIR /root/handwriting-synthesis
RUN pip install -r requirements.txt

# Launch image in shell
CMD bash
