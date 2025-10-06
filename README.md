# Personal Health Agent (PHA) - Multi-Agent System

A Python implementation of the multi-agent Personal Health Agent system based on the research paper ["The Anatomy of a Personal Health Agent"](https://arxiv.org/abs/2508.20148).

## 🎯 Overview

This system uses three specialized AI agents that collaborate to provide personalized health insights and coaching:

1. **Data Science Agent (DS)** - Analyzes time-series wearable and health data, performs statistical analysis
2. **Domain Expert Agent (DE)** - Provides medical context and health interpretations
3. **Health Coach Agent (HC)** - Guides users toward health goals using motivational coaching strategies

An **Orchestrator** coordinates these agents through a 4-step process:
- **User Need Understanding** - Analyzes queries to determine required agents
- **Agent Orchestration** - Routes tasks to main/supporting agents
- **Query Reflection** - Reviews responses for quality and completeness
- **Memory Update** - Maintains conversation context

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                            │
│  (4-step coordination: Understand → Route → Reflect → Log)  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ DS Agent │  │ DE Agent │  │ HC Agent │
│ (Stats)  │  │ (Medical)│  │ (Coach)  │
└──────────┘  └──────────┘  └──────────┘
```

## 📁 Project Structure

```
gpha/
├── api_client.py      # Gemini API wrapper
├── prompts.py         # Jinja2 prompt templates for all agents
├── agents.py          # DataScienceAgent, DomainExpertAgent, HealthCoachAgent
├── orchestrator.py    # Multi-agent coordination logic
├── mock_data.py       # Simulated health/wearable data for testing
├── main.py           # Entry point with demo modes
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd gpha

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up API Key

Set your Google Gemini API key as an environment variable:

```bash
# For bash/zsh (Linux/Mac)
export GOOGLE_API_KEY='your-api-key-here'

# For Windows Command Prompt
set GOOGLE_API_KEY=your-api-key-here

# For Windows PowerShell
$env:GOOGLE_API_KEY='your-api-key-here'
```

Or add it to your shell configuration file (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Run the System

```bash
# Run interactive conversation mode (default)
python main.py
python main.py interactive

# Run flow visualization mode (shows agent orchestration)
python main.py flow
python main.py flow "How has my sleep quality been this month?"

# View mock data summary
python main.py data
```

### 4. Test the API Client

```bash
# Test Gemini API connection
python api_client.py
```

## 📊 Mock Data

The system includes realistic simulated health data:
- **Wearable Data**: 30 days of heart rate, sleep, activity, HRV
- **Health Records**: Conditions, medications, allergies, family history
- **Lab Results**: Cholesterol, glucose, HbA1c, Vitamin D, etc.
- **User Profile**: Age, gender, height, weight, activity level

View the data summary:
```bash
python mock_data.py
```

