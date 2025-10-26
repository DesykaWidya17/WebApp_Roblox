FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY roblox_webapp.py .
EXPOSE 5000
CMD ["python", "roblox_webapp.py"]
