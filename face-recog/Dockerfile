FROM docker.io/oraclelinux:9

# Install CUDA
RUN dnf install -y yum-utils && \
    dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo && \
    dnf clean all
RUN dnf -y install cuda-toolkit-12-3 && \
    dnf clean all       

# Install development tools and other dependencies 
RUN yum install -y \
    python3.12 \
    python3.12-devel \
    cmake \
    gcc-c++ \
    wget \
    unzip    

# This links 'python3' to 'python3.12' and 'pip3' to 'pip3.12'
RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    alternatives --set python3 /usr/bin/python3.12 && \
    python3 -m ensurepip && \
    python3 -m pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt .

# Install python & the python dependencies
# Install python3-pip and other dependencies
RUN dnf install -y python3-pip && \
    dnf clean all
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
RUN mkdir /app
COPY src/ /app
WORKDIR /app

# Run the application
CMD ["python3", "/app/main.py"]
