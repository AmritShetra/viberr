FROM python:3.8.0

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /src/

# Copy project
COPY . /src/

# Install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/src/entrypoint.sh"]

