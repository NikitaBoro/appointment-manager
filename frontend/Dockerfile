FROM python:3.10.14

WORKDIR /app

RUN apt-get update && apt-get install -y tzdata

ENV TZ=Asia/Jerusalem

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
