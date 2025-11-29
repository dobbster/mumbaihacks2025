# Frontend - Misinformation Detection System

React + Vite frontend for the misinformation detection system.

## Overview

The frontend provides a user-friendly interface to interact with the misinformation detection backend API. Users can enter queries to verify claims and receive classification results with confidence scores and source attribution.

## Features

- **Search Interface**: Enter queries to verify claims
- **Real-time Processing**: Shows loading state during API calls
- **Results Display**: Shows classification results with:
  - Classification verdict (misinformation/legitimate/uncertain)
  - Confidence score
  - Source URLs (limited to 5)
  - Evidence and reasoning
- **Error Handling**: Displays user-friendly error messages

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file (optional):
```bash
VITE_API_BASE_URL=http://localhost:2024
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## API Integration

The frontend connects to the backend API at `/verify` endpoint:

- **Base URL**: `http://localhost:2024` (default) or set via `VITE_API_BASE_URL`
- **Endpoint**: `POST /verify`
- **Request**: `{ "prompt": "user query", "max_results": 5 }`
- **Response**: Classification results with sources and confidence scores

## Components

- **SearchNav.jsx**: Main search interface and results display
- **HomePage.jsx**: Landing page
- **Navbar.jsx**: Navigation bar
- **LiveFeed.jsx**: Live feed component
- **NewsAssistant.jsx**: News assistant component
- **Globe.jsx**: Globe visualization component
- **Contributors.jsx**: Contributors information

## Services

- **api.js**: API service for backend communication
  - `verifyMisinformation(prompt, maxResults)`: Main verification function
  - `checkHealth()`: Health check function

## Build

To build for production:

```bash
npm run build
```

The built files will be in the `dist/` directory.
