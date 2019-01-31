FROM python:alpine
RUN apk add --no-cache git
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY greetings.txt /app/
COPY app.py /app/ 
ENTRYPOINT ["python"]
CMD ["app.py"]
