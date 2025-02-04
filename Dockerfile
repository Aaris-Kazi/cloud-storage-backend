# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .

RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-confi

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid 10001 --create-home appuser

USER 10001

WORKDIR /app
COPY . /app

COPY /run/etc.xml /app/run/etc.xml
COPY /run/ca.pem /app/run/ca.pem


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cloud_drive.wsgi"]
