# Dockerfile
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required tools
RUN apt update && apt install -y python3 python3-pip iputils-ping net-tools

# Set workdir
WORKDIR /app/port_scanner

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copy the rest of the source code
COPY . /app

# Default to keep the container alive
CMD ["tail", "-f", "/dev/null"]
