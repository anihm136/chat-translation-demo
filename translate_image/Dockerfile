FROM python:latest

WORKDIR /translate-app

ADD . .
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/libindic/indic-trans.git

EXPOSE 8000
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
