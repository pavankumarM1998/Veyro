# **VEYRO: REAL-TIME DATA ENGINEERING PROJECT**

### **Live Application URL:** [https://fair-vehicle.web.app](https://fair-vehicle.web.app)

![Project Architecture](https://github.com/pavankumarM1998/Veyro/blob/main/architecture.png)

## **About Veyro**
* **Pronounced:** *VAY-ro*
* **Inspiration:** Inspired by **Velocity** (speed) and **Way** (travel, route), combined with the modern tech-style ending **"-ro"**.
* **Brand Meaning:** Fast, reliable, and smart mobility.
* **Taglines:** 
  * *Every Ride. Every Way.*
  * *Ride Smarter.*
  * *Move Without Limits.*

Veyro is an end-to-end real-time data engineering project simulating a high-throughput ride-booking platform (similar to Uber). It ingests real-time ride transactions and processes them through a multi-tier streaming pipeline on Azure.

---

## **System Architecture**
1. **Frontend UI & Event Producer (FastAPI):** A user-facing web portal that simulates ride bookings. Dynamic ride data (passenger details, fare calculation, coordinates) is generated on the fly.
2. **Ingestion Layer (Azure Event Hubs):** FastAPI sends the generated ride JSON records to Azure Event Hubs (a Kafka-compatible streaming ingestion service) in real-time.
3. **Data Lake Storage (ADLS Gen 2):** Stores raw (Bronze), cleaned (Silver), and aggregated (Gold/OBT) Delta tables.
4. **Processing Layer (Azure Databricks / PySpark):** 
   * **Bronze Layer:** Consumes the streaming data from Event Hubs and writes the raw JSON payloads into Delta Lake.
   * **Silver Layer:** Decodes the JSON schemas, enforces quality rules, handles nulls, and standardizes data.
   * **Gold (OBT - One Big Table):** Joins dimension lookups with ride events to create a unified One Big Table (OBT) for high-performance BI reporting.
5. **Orchestration (Azure Data Factory):** Orchestrates metadata-driven ingestion pipelines and bulk data movements.

---

## **How to Run Locally**

1. **Activate the Virtual Environment:**
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   CONNECTION_STRING="Endpoint=sb://<your-eventhub-namespace>.servicebus.windows.net/;SharedAccessKeyName=Sendpolicy;SharedAccessKey=<your-key>;EntityPath=<your-topic>"
   EVENT_HUBNAME="<your-topic>"
   ```
4. **Start the FastAPI Web App:**
   ```powershell
   python api.py
   ```
   Open `http://localhost:8000` in your browser.
