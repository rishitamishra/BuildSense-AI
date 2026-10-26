# 🏗️ BuildSense AI — Multimodal Construction Intelligence

BuildSense AI is an AI-powered construction intelligence platform designed to help users understand construction site conditions, identify potential safety hazards, assess visible cracks, estimate project costs, plan construction activities, and obtain preliminary property valuation insights.

The platform combines image-based analysis with project details to generate structured, actionable insights for construction planning and site monitoring.

## ✨ Features

- **🦺 Construction Safety Analysis:** Identifies potential site hazards and recommends preventive actions.
- **🧱 Crack Detection & Assessment:** Analyzes uploaded site images for visible cracks, estimates their severity, and suggests possible causes and next steps.
- **📅 Construction Planning:** Generates preliminary project timelines, milestones, material estimates, and indicative construction costs.
- **💰 Property Valuation:** Provides preliminary valuation insights based on supplied project information and assumptions.
- **📷 Multimodal Image Analysis:** Accepts construction site images along with project descriptions and details.
- **💡 Site Recommendations:** Provides practical guidance for site safety, documentation, and construction management.
- **🔄 Demo Mode:** Returns sample results when the Gemini API key is not configured.

## 🛠️ Technology Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Pydantic
- Google Gemini API
- Uvicorn

**Tools**
- Git and GitHub
- Visual Studio Code
- Python virtual environment
- Node.js and npm

## 🏛️ Project Structure

```text
BuildSense-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

*The structure above illustrates the expected layout; adjust it if your actual repository differs.*

## ⚙️ Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version supported by the installed dependencies
- Node.js and npm
- Git
- A Google Gemini API key for AI-powered image analysis

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/rishitamishra/BuildSense-AI.git
cd BuildSense-AI
```

### 2. Set Up the Backend

Open a terminal in the project root and navigate to the backend:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory using `.env.example` as a reference.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Replace the placeholder with your own valid API key. Never commit `.env` or expose API credentials publicly.

### 4. Start the Backend Server

From the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

The backend should start at:

- API base URL: `http://127.0.0.1:8000`
- Health check: `http://127.0.0.1:8000/api/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

### 5. Set Up the Frontend

Open a second terminal at the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, typically:

`http://localhost:5173`

Keep both development servers running while testing the application.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Checks backend status and whether the Gemini API key is configured |
| POST | `/api/analyze` | Analyzes project details and uploaded construction images |

The analysis endpoint accepts multipart form data containing a project description, project details, and optional image files.

## 🔍 How It Works

1. The user enters construction project details and a site description.
2. The user uploads relevant construction site images.
3. The backend validates the submitted data and image files.
4. If configured, the Gemini API analyzes the provided information and images.
5. The backend returns structured JSON containing safety findings, crack assessment, planning estimates, valuation insights, and site recommendations.
6. The frontend presents the results to the user.

If the Gemini API key is not configured, the backend returns illustrative demo-mode results instead of analyzing image contents.

## 🎯 Use Cases

- Preliminary construction site safety reviews
- Visual inspection support for cracks and surface damage
- Early-stage construction budgeting and planning
- Material quantity and cost estimation
- Construction progress documentation
- Preliminary property valuation support

## 🔮 Future Enhancements

Potential improvements include:

- Construction progress tracking using repeated site images
- Weather API integration
- Location-specific construction cost data
- Interactive dashboards and downloadable reports
- Project history and inspection records
- Improved risk prioritization and reporting
- Integration with professional inspection workflows

## ⚠️ Limitations and Disclaimer

BuildSense AI is intended as a preliminary decision-support tool. Its outputs are estimates and may be incomplete or inaccurate.

- Image analysis cannot establish structural safety or diagnose cracks conclusively.
- Cost and timeline estimates depend on project inputs and local conditions.
- Property valuations require verified market data and professional assessment.
- Live weather and property market data are not automatically available unless separately integrated.
- Critical safety concerns and suspected structural damage must be reviewed by qualified professionals.

**BuildSense AI does not replace licensed structural engineers, safety officers, contractors, or professional property valuers.**

## 👩‍💻 Author

**Rishita Mishra**

GitHub: [@rishitamishra](https://github.com/rishitamishra)

Project Repository: [BuildSense-AI](https://github.com/rishitamishra/BuildSense-AI)

## 📄 License

No license has been specified yet. Add a `LICENSE` file if you intend to distribute this project under an open-source license.
