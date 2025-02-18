FROM oraclelinux:8

# Install Oracle Instant Client
RUN  dnf -y install oracle-instantclient-release-23ai-el8 && \
     dnf -y install oracle-instantclient-basic oracle-instantclient-devel oracle-instantclient-sqlplus && \
     rm -rf /var/cache/dnf

# Install dependencies
RUN yum install -y \
    python39 \
    python39-devel \
    python39-tkinter \
    cmake \
    gcc-c++ \
    wget \
    unzip \
    mesa-libGL \
    qt5-qtbase qt5-qtbase-gui qt5-qtx11extras

# Copy the requirements file
COPY requirements.txt .

# Install the python dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
RUN mkdir /app
COPY src/ /app
WORKDIR /app

# Run the application
CMD ["python3", "/app/capture.py"]


# FOR DEBUG
# Install required packages for video support
# RUN yum install -
#CMD ["/usr/bin/xterm","-display",":0"]
