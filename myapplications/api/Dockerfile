#FROM python:3.11-slim

#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1

#WORKDIR /myapplications

#COPY requirements.txt .

#RUN pip install --upgrade pip \
#    && pip install --no-cache-dir -r requirements.txt

#COPY . .

#EXPOSE 8000

#CMD ["uvicorn", "myapplications.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /myapplications
COPY . .

# install dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .


# Expose the port FastAPI will run on
EXPOSE 8000

ENV PYTHONPATH=/api
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]