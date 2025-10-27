# Gunakan Python base image
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Copy semua file dari project ke dalam container
COPY . .

# Install dependencies Flask
RUN pip install --no-cache-dir flask

# Expose port Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "roblox_webapp.py"]
