# Stage 1: build dependencies
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10 as base

WORKDIR /workspace

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "-c", "uvicorn attendance_app.main:app --host 0.0.0.0 --reload;"]
