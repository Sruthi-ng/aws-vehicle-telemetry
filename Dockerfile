# Use a lightweight Python base image (Simulates an ECU environment)
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for caching speed)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and the certificates folder
COPY vehicle_sim.py .
COPY certs/ ./certs/

# Command to run when the container starts
CMD ["python", "vehicle_sim.py"]