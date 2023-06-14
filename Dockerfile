FROM ubuntu:22.04
ARG VEnv=WebAppPy38
ARG PyVersion=3.8
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
WORKDIR /app

# Install dependencies and utilities
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    apt-transport-https \
    curl

# Download and install the ODBC Driver 18 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/msprod.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Install unixODBC
RUN apt-get install -y unixodbc

# Set ODBC configurations
RUN echo "export PATH=\$PATH:/opt/mssql-tools/bin" >> ~/.bashrc \
    && echo "/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so" >> /etc/odbcinst.ini

# Install miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
    && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
    && echo "conda activate base" >> ~/.bashrc

# Create Conda environment
RUN /opt/conda/bin/conda create -y --name $VEnv python=3.8

# Activate Conda environment
ENV PATH="/opt/conda/envs/$VEnv/bin:$PATH"

# copy directory
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]