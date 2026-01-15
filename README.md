#   SafeRouteX Disaster-Aware Evacuation Routing System

> SafeRouteX computes risk-aware evacuation routes using live weather and seismic data, built for backend engineers, researchers, and emergency-planning system designers.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)
[![Contributors](https://img.shields.io/badge/contributors-0-blueviolet)](#)

---


## About
SafeRouteX exists to address the problem that during disasters, the shortest route is often unsafe. It computes evacuation paths that account for real-time risk factors such as heavy rainfall and nearby seismic activity, rather than distance alone. By modeling regions as a graph with dynamically penalized risks, it helps planners, researchers, and backend-focused engineers explore safer evacuation strategies and disaster-aware routing systems.

---
## Features

- **Risk-aware evacuation routing**: Computes evacuation paths that minimize risk rather than distance using dynamic penalties.
- **Live disaster data integration**: Incorporates real-time rainfall (Open-Meteo) and earthquake data (USGS).
- **Graph-based modeling**: Represents regions as a weighted graph to enable flexible and extensible routing logic.
- **Safehouse discovery**: Identifies nearby shelters and critical facilities for evacuation endpoints.
- **Minimal interactive UI**: Provides a lightweight Gradio interface with map visualization for demonstration.

---

## Tech Stack

- **Language**: Python  
- **Frameworks / Libraries**: FastAPI, NetworkX, Gradio, Folium, Requests  
- **Geospatial / Data APIs**: OpenStreetMap (Nominatim), Open-Meteo, USGS Earthquake API  
- **Containerization**: Docker  
- **Deployment**: Single-container service (Render / Railway / VPS compatible)

---



