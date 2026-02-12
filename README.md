---

# 🕵️‍♂️ CrimeLens: Intelligent Crime Analytics & Safe Navigation

CrimeLens is a **full-stack geospatial intelligence platform** designed to analyze crime data, predict risks, and provide **safe navigation routes**.
It combines **advanced 2D/3D visualization**, **machine learning forecasting**, and **public sentiment analysis** into a unified, interactive dashboard.

Built with **FastAPI (Python)** and **React**, CrimeLens integrates **Google Gemini AI** for natural language insights and **OSMnx** for intelligent street-network routing.

---

## ✨ Key Features

### 📍 Unified Interactive Map

* 2D visualization using **Leaflet**
* Toggleable layers:

  * Crime heatmaps
  * Hotspots (K-Means clustering)
  * Police stations
  * Hospitals

### 🛡️ Safe Navigation Routing

* Calculates **Fastest** vs **Safest** walking routes
* Uses **Dijkstra’s algorithm**
* Edge weights adjusted by local crime density

### 🏙️ 3D Crime Density Mapping

* Immersive **3D Hexbin visualization**
* Built using **Deck.gl**
* Highlights high-density crime zones

### 📈 Predictive Analytics

* **Time-Series Forecasting**

  * Uses **Facebook Prophet**
  * Predicts crime trends for the next 12 months
* **Risk Modeling**

  * **XGBoost classifier**
  * Determines crime severity based on location and time

### 📰 Public Sentiment Engine

* NLP analysis of local news headlines
* Uses **TextBlob**
* Computes:

  * Sentiment score
  * **Public Fear Index**

### 🤖 AI Safety Assistant

* Chat-based safety assistant
* Powered by **Google Gemini**
* Provides:

  * Safety tips
  * Area summaries
  * Risk explanations

### 📄 Automated Reporting

* One-click **PDF crime intelligence reports**

---

## 🛠️ Tech Stack

### Backend

* **Framework:** FastAPI
* **Data Processing:** Pandas, NumPy
* **Machine Learning:**

  * Scikit-learn (K-Means)
  * XGBoost
  * Prophet
* **Geospatial:** OSMnx, NetworkX
* **AI / NLP:** Google Generative AI (Gemini), TextBlob

### Frontend

* **Framework:** React (Create React App)
* **Styling:** Tailwind CSS, Headless UI
* **Visualization:**

  * Deck.gl
  * React-Leaflet
  * Chart.js
  * OGL (WebGL shaders)
* **State & Networking:** Axios

---

## 🚀 Getting Started

### Prerequisites

* Python **3.9+**
* Node.js **16+**
* Git

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/crimelens.git
cd crimelens
```

---

### 2️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Configuration (`.env`)

Create a `.env` file inside the `backend/` directory:

```env
# Required for AI features
GOOGLE_API_KEY=your_google_gemini_key

# Optional: News sentiment analysis
NEWS_API_KEY=your_newsapi_org_key
```

#### Run the Backend Server

```bash
uvicorn app.main:app --reload
```

📍 Backend available at:
`http://localhost:8000`

---

### 3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the frontend
npm start
```

📍 Frontend available at:
`http://localhost:3000`

---

## 📊 Data Format

Upload a CSV file via the sidebar.
The system works best with **LAPD-style datasets**, but any CSV with the following columns is supported:

| Column Name | Description        | Example       |
| ----------- | ------------------ | ------------- |
| DATE OCC    | Date of occurrence | 01/20/2024    |
| TIME OCC    | Time (24h)         | 1330 or 13:30 |
| LAT         | Latitude           | 34.0522       |
| LON         | Longitude          | -118.2437     |
| Crm Cd Desc | Crime description  | BURGLARY      |
| AREA NAME   | Area / District    | Central       |

> **Note:** If `Severity` is not provided, CrimeLens computes it automatically based on crime type.

---

## 🧭 Usage Guide

1. **Upload Data**
   Upload a CSV file from the sidebar.

2. **Apply Filters**
   Filter by:

   * Area
   * Crime type
   * Severity

3. **Explore the Map**

   * Toggle layers (heatmap, hotspots, services)
   * Click **Start Navigation** to select source & destination
   * Compare safest vs fastest routes

4. **3D View**

   * Switch to the **3D Density tab**
   * Use `Ctrl + Click` to rotate the map

5. **Analytics**

   * View crime forecasts in the **Time-Series tab**
   * Analyze sentiment in the **Public Sentiment tab**

6. **AI Assistant**

   * Click the floating chat button
   * Ask questions like:

     > “Is this area safe at night?”

---

## 📂 Project Structure

```plaintext
crimelens/
├── backend/
│   ├── app/
│   │   ├── services/      # ML, Routing, Analytics Logic
│   │   ├── main.py        # FastAPI entry point
│   │   └── models.py     # Pydantic schemas
│   └── requirements.txt
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── services/     # API connectors
│       ├── views/        # Dashboard views
│       └── App.js
└── README.md
```

---

## ⚠️ Notes

* **First Routing Request:**
  OSMnx downloads OpenStreetMap data on first use (10–20 seconds).

* **Browser Requirements:**
  WebGL-enabled browser required (Chrome, Firefox, Edge).

---

## 🤝 Contributing

Contributions are welcome 🎉
Feel free to open an issue or submit a pull request for improvements or bug fixes.

---

## 📄 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

---
