FROM python:3.11.4
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot
COPY . /usr/src/bot
RUN ["/bin/bash", "-c", "pip install --no-cache-dir -r requirements.txt"]
CMD ["python", "bot.py"]
