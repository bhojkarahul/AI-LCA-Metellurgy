AI-Driven LCA Prototype
This repository contains a simple, single-file prototype for an AI-Driven Life Cycle Assessment (LCA) Tool for the metallurgy and mining industries. Developed as part of the Smart India Hackathon 2025, this project demonstrates a modern approach to sustainability analysis by integrating AI/ML concepts with traditional LCA methodologies.

Idea & Motivation
Traditional LCA is a manual, time-consuming process often limited by incomplete data. Our project aims to solve this by creating an intuitive, AI-powered platform that makes LCA faster, more accessible, and focused on driving a circular economy. This prototype showcases the core functionality, including:

Automated Analysis: Performing a complete LCA from a few user inputs.

Intelligent Insights: Providing contextual data, hotspot analysis, and a high-level sustainability scorecard.

User-Friendly Interface: Presenting complex data through a clean, modern dashboard with charts and historical data.

Working
The prototype is built as a single-file Flask web application to demonstrate the core features without complex setup.

Core Functionality
User Input: The user selects a metal (virgin or recycled) and a quantity.

Data Processing: The Flask application uses a simplified data model to calculate key metrics like carbon footprint, water usage, and energy consumption.

Overall Scorecard: The results page displays a color-coded sustainability score, giving an immediate, at-a-glance view of the product's environmental performance.

History & Analysis: The homepage includes a history section to track previous analyses. The results page provides a detailed breakdown of impact by life cycle stage, identifying the biggest "hotspot."

What-If Scenario: A key feature that shows the power of the tool is a dynamic comparison between using a virgin material versus a recycled one, demonstrating the value of a circular economy.

Algorithm
To run this prototype locally, follow these simple steps.

Prerequisites
You need to have Python and pip installed on your system.

Installation
Clone the Repository: Download this project to your local machine.

Create a Virtual Environment: Open your terminal and navigate to the project directory. It's a good practice to create a virtual environment to manage dependencies:

python -m venv venv

Activate the Environment:

On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate

Install Dependencies: Install the required Python libraries:

pip install Flask Jinja2

Usage
Run the Application: With your virtual environment activated, run the main Python file:

python app.py

View in Browser: Open a web browser and navigate to the URL provided in the terminal, typically http://127.0.0.1:5000.

Project Structure
The project is designed to be self-contained within a single file for simplicity.

/LCA_prototype/
├── venv/                   # Python virtual environment
├── app.py                  # The main Flask application (all logic and templates)
└── README.md               # This file


