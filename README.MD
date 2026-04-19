# AI Travel Agent 🧳

**Plan smarter trips with AI-powered itineraries — no local models, no heavy setup.**

---

## Overview

AI Travel Agent is a full-stack web application that helps users plan personalised travel itineraries using the power of large language models. Users describe their trip in natural language — destination, budget, travel dates, preferences — and the system generates a structured, actionable itinerary in seconds.

The backend is built in **Python (FastAPI)** and communicates with **OpenRouter** to access state-of-the-art LLMs via a simple API key — no local Ollama instance, no multi-gigabyte model downloads, no GPU required. The frontend is a modern **Next.js** application with a polished UI designed to feel like a premium travel product, not a demo.

This architecture makes the application easy to develop locally, straightforward to deploy, and accessible to contributors regardless of their hardware.

---

## Demo / Preview

> **Live Demo:** _[Add your deployed frontend URL here — e.g., https://ai-travel-agent.vercel.app]_

### 🏠 Landing Page
The hero screen with the "The World, Perfectly Curated" tagline and a single CTA to start planning.

![Landing Page](docs/screenshots/ChatGPT%20Image%20Apr%2019%2C%202026%2C%2007_50_15%20PM.png)

### 📋 Day-by-Day Itinerary Plan
AI-generated itinerary shown alongside the input form. Each day has a themed title with bullet-point activities.

![Itinerary Plan](docs/screenshots/ChatGPT%20Image%20Apr%2019%2C%202026%2C%2007_51_21%20PM.png)

### 🗺️ Trip Overview — Key Places & Booking Links
Destination summary card with duration, estimated budget, and a grid of key places with OSM/Google Maps deep links and a ticket discovery panel.

![Trip Overview](docs/screenshots/ChatGPT%20Image%20Apr%2019%2C%202026%2C%2007_50_01%20PM.png)

### 💰 Places & Budget Breakdown
Expanded key places list with category tags alongside a per-person daily cost breakdown (hotel, food, transport, activities).

![Places and Budget](docs/screenshots/ChatGPT%20Image%20Apr%2019%2C%202026%2C%2007_50_05%20PM.png)

---

## Features

- **Natural language trip planning** — describe your trip in plain text and receive a structured itinerary
- **Budget-aware itinerary generation** — the AI accounts for budget tiers (budget, mid-range, luxury) when generating recommendations
- **Seasonal and date-based planning** — recommendations adapt to weather, local events, and peak/off-peak travel periods
- **User refinement flow** — iterate on the generated plan with follow-up prompts without starting over
- **Location and map support** — places, landmarks, and routes are surfaced with context for easy discovery
- **Travel ratings and info integration** — enriched recommendations pulled from structured data sources
- **OpenRouter-based LLM access** — no local model required; configure a model and API key in your `.env` file
- **Modular Python backend** — clean separation of concerns between LLM client, prompt engineering, and API routing
- **Modern Next.js frontend** — responsive, accessible, and designed with a premium UI/UX

---

## Tech Stack

### Frontend
- [Next.js 14](https://nextjs.org/) — React framework with App Router
- [React](https://react.dev/) — component-based UI
- [TypeScript](https://www.typescriptlang.org/) — type-safe development
- [Tailwind CSS](https://tailwindcss.com/) — utility-first styling

### Backend
- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — async REST API framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management
- [httpx](https://www.python-httpx.org/) — async HTTP client for LLM API calls

### AI / LLM
- [OpenRouter](https://openrouter.ai/) — unified LLM API gateway
  - Supports models from OpenAI, Anthropic, Google, Meta, Mistral, and others
  - No local model installation required

### APIs / Data Sources
- OpenRouter API — LLM inference
- _(Optional)_ SerpAPI — real-time travel data, hotel results, attractions
- _(Optional)_ Maps / geocoding APIs

### Deployment
- **Frontend:** [Vercel](https://vercel.com/)
- **Backend:** [Render](https://render.com/)

---

## Folder Structure

```
ai_travel_agent/
├── frontend/                  # Next.js application
│   ├── app/                   # App Router pages and layouts
│   │   ├── page.tsx           # Landing / home page
│   │   ├── plan/              # Trip planning and itinerary pages
│   │   └── layout.tsx         # Root layout
│   ├── components/            # Reusable UI components
│   ├── lib/                   # API client utilities
│   ├── public/                # Static assets
│   ├── .env.local.example     # Frontend environment variable template
│   └── package.json
│
├── backend/                   # FastAPI application
│   ├── main.py                # FastAPI app entry point and route registration
│   ├── config.py              # Environment configuration and validation
│   ├── llm_client.py          # OpenRouter LLM client
│   ├── services/              # Business logic (itinerary, seasonality, budget)
│   │   ├── itinerary.py
│   │   ├── seasonality.py
│   │   └── budget.py
│   ├── routers/               # API route modules
│   │   └── travel.py
│   ├── .env.example           # Backend environment variable template
│   └── requirements.txt
│
├── docs/                      # Documentation, screenshots, diagrams
│   └── screenshots/
│
└── README.md
```

---

## How It Works

```
User Input (frontend)
       │
       ▼
Next.js frontend collects trip details
(destination, dates, budget, preferences)
       │
       ▼
POST /api/plan-trip  →  FastAPI backend
       │
       ▼
Backend builds a structured prompt
and calls OpenRouter API
       │
       ▼
OpenRouter routes to the configured LLM
(e.g., Mistral, GPT-4o, Llama 3, etc.)
       │
       ▼
Backend parses the LLM response into
a structured itinerary JSON object
       │
       ▼
Frontend renders the itinerary
with refinement options available
```

The backend is stateless per request. Refinement works by re-sending the original context plus user feedback in subsequent API calls.

---

## Local Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- An [OpenRouter](https://openrouter.ai/) API key (free tier available)

---

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-travel-agent.git
cd ai-travel-agent
```

---

### 2. Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OpenRouter API key

# Start the backend server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs are served at `http://localhost:8000/docs`.

---

### 3. Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local and set the backend URL

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

---

## Environment Variables

### Backend — `backend/.env`

```env
# Required — your OpenRouter API key
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxx

# Optional — override the OpenRouter base URL (default: https://openrouter.ai/api/v1)
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Optional — the model to use (default: mistralai/mistral-7b-instruct)
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
```

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Yes | Your OpenRouter API key. Create one at [openrouter.ai/keys](https://openrouter.ai/keys) |
| `OPENROUTER_BASE_URL` | No | Base URL for the OpenRouter API. Rarely needs to change |
| `OPENROUTER_MODEL` | No | The model identifier to use for generation. See [openrouter.ai/models](https://openrouter.ai/models) for available options |

---

### Frontend — `frontend/.env.local`

```env
# URL of the running backend API
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | ✅ Yes | The base URL of the FastAPI backend. Change this to your production URL when deploying |

---

## Deployment

### Frontend → Vercel

1. Push your repository to GitHub.
2. Import the project into [Vercel](https://vercel.com/new).
3. Set the **Root Directory** to `frontend/`.
4. Add the following environment variable in the Vercel project settings:
   ```
   NEXT_PUBLIC_BACKEND_URL=https://<your-backend>.onrender.com
   ```
5. Deploy. Vercel handles builds and CDN distribution automatically.

---

### Backend → Render

1. Create a new **Web Service** on [Render](https://render.com/).
2. Connect your GitHub repository and set the **Root Directory** to `backend/`.
3. Set the build command:
   ```
   pip install -r requirements.txt
   ```
4. Set the start command:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Add the following environment variables in the Render dashboard:
   ```
   OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxx
   OPENROUTER_MODEL=mistralai/mistral-7b-instruct
   ```
6. Deploy. Render will assign a public URL to your backend service.

> **Note:** Once the backend is deployed, update `NEXT_PUBLIC_BACKEND_URL` in your Vercel environment settings to point to the Render service URL and redeploy the frontend.

---

## Roadmap

The following improvements are planned or under consideration:

- [ ] **Flight and hotel booking deep-links** — Surface direct booking links from aggregators like Skyscanner or Booking.com
- [ ] **Hotel comparison cards** — Compare options by price, rating, and distance from key attractions
- [ ] **Enhanced map intelligence** — Interactive maps with route visualisation and point-of-interest clustering
- [ ] **User authentication and saved trips** — Allow users to create accounts and persist itineraries
- [ ] **Response caching** — Cache frequently requested routes and destinations to reduce LLM API costs
- [ ] **Export and share** — Download itineraries as PDF or share via a unique link
- [ ] **Multilingual support** — Generate itineraries in the user's preferred language
- [ ] **Admin analytics dashboard** — Track usage patterns and popular destinations
- [ ] **Real-time travel alerts** — Surface advisories, visa requirements, and seasonal warnings
- [ ] **Multi-city trip planning** — Support complex itineraries spanning multiple destinations
