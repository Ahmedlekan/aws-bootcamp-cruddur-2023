FROM python:3.10-slim-bookworm AS build

WORKDIR /backend-flask

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .


FROM python:3.10-slim-bookworm

WORKDIR /backend-flask

ENV FLASK_ENV=production
ENV PORT=5000
ENV PYTHONPATH=/backend-flask

COPY --from=build /install /usr/local
COPY --from=build /backend-flask /backend-flask

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]



