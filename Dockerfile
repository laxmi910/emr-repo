FROM python:3.9.2
RUN pip install --upgrade pip
WORKDIR /app
#COPY patient.py /app/patient.py
#COPY templates ./
COPY requirements.txt .
#install dependencies
RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
COPY . .
CMD ["python","patient.py"]
