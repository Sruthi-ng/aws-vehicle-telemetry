# AWS Serverless Vehicle Telemetry Pipeline

## Project Overview
This project simulates a **Connected Vehicle (IoT)** architecture. It generates real-time vehicle telemetry data (Engine RPM, Speed, Battery Voltage, Coolant Temp), transmits it securely to the Cloud, and triggers automated alerts based on critical events.

The goal was to bridge the gap between **Embedded Systems** (HIL/Validation) and **Modern Cloud Infrastructure** (AWS/DevOps).

## Architecture
**[Vehicle Simulator (Docker)]** → *MQTT (TLS 1.2)* → **[AWS IoT Core]** → *Rules Engine* → **[AWS Lambda]** → *SNS* → **[Email Alert]**

* **Edge:** Python script running in a Docker Container (simulating an ECU).
* **Protocol:** MQTT over Secure WebSockets (Port 443/8883).
* **Cloud Ingestion:** AWS IoT Core.
* **Serverless Compute:** AWS Lambda (Python 3.9) for payload decoding and logic checks.
* **Notification:** Amazon SNS for critical "Overheating" alerts.

## Tech Stack
* **Languages:** Python 3.9
* **Infrastructure:** Docker, AWS (IoT Core, Lambda, SNS, IAM)
* **Libraries:** `AWSIoTPythonSDK`, `boto3`, `json`
* **Security:** X.509 Certificate-based authentication.

## How It Works
1.  The `vehicle_sim.py` script generates random driving data.
2.  If `engine_coolant_temp` exceeds **105°C**, the simulator flags a warning.
3.  Data is serialized to **JSON** and published to the topic `vehicle/telemetry`.
4.  **AWS IoT Core** receives the message and triggers an IoT Rule.
5.  The Rule invokes an **AWS Lambda** function.
6.  Lambda checks the temperature; if critical, it publishes to an **SNS Topic**.
7.  The System Admin receives an immediate Email/SMS alert.

## How to Run Locally
*(Note: AWS Certificates are required to run this simulation and are not included in this repo for security.)*

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/aws-vehicle-telemetry.git](https://github.com/YOUR_USERNAME/aws-vehicle-telemetry.git)
    cd aws-vehicle-telemetry
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Add Certificates:**
    * Place your AWS IoT certificates (private key, certificate, root CA) in a `certs/` folder.

4.  **Run the Simulator:**
    ```bash
    python vehicle_sim.py
    ```

## Docker Usage
To simulate a containerized deployment:
```bash
docker build -t vehicle-sim .
docker run vehicle-sim
