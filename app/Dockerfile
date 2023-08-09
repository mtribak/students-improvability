
FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8501

COPY . .

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
