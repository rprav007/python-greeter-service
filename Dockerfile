FROM python:alpine
RUN apk add --no-cache git
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
<<<<<<< HEAD
COPY greetings.txt /app/
COPY app.py /app/ 
=======
USER 1001
>>>>>>> 8bef756c8a935ae33e6a959fc87392cea393a93e
ENTRYPOINT ["python"]
CMD ["app.py"]
