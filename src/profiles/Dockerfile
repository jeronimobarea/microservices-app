FROM python:3

WORKDIR /server/src/profiles

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn main:app --reload --port 8100" ]