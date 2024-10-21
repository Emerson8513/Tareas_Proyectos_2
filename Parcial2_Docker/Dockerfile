FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libpq-dev gcc cmake weasyprint libgl1-mesa-glx libglib2.0-0 git

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
