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
# Run demo mode (2 sample queries)
python main.py

# Run interactive conversation mode
python main.py interactive

# Run all sample queries in batch
python main.py batch

# Run a single custom query
python main.py single "How has my sleep quality been this month?"

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

## 🎮 Usage Examples

### Interactive Mode

```bash
$ python main.py interactive

You: How has my sleep quality been over the past month?

PHA: Based on my analysis of your sleep data over the past 30 days...
[Detailed response combining DS analysis, DE medical insights, and HC coaching]

You: I want to improve my cardiovascular health.

PHA: I'd love to help you with that goal! Let me ask you a few questions...
```

### Single Query Mode

```bash
python main.py single "What does my heart rate variability data suggest about my stress levels?"
```

### Batch Demo

```bash
python main.py batch
# Runs all 8 sample queries sequentially
```

## 🔧 Components

### API Client ([api_client.py](api_client.py))

Wrapper for Google Gemini API:
```python
from api_client import call_gemini

response = call_gemini(
    system_prompt="You are a health expert...",
    user_prompt="Analyze this data...",
    temperature=0.5
)
```

### Agents ([agents.py](agents.py))

#### Data Science Agent
```python
ds_agent = DataScienceAgent(personal_data=user_data)
result = ds_agent.analyze_query("How has my sleep changed?")
# Returns: {'analysis_plan': ..., 'analysis_code': ...}
```

#### Domain Expert Agent
```python
de_agent = DomainExpertAgent(user_health_context=health_context)
answer = de_agent.answer_health_question("What is my diabetes risk?")
```

#### Health Coach Agent
```python
hc_agent = HealthCoachAgent(user_context=user_profile)
response = hc_agent.identify_goals(
    user_message="I want to get healthier",
    health_insights=insights
)
```

### Orchestrator ([orchestrator.py](orchestrator.py))

Coordinates all agents:
```python
orchestrator = Orchestrator(ds_agent, de_agent, hc_agent)
result = orchestrator.process_query("Help me lose weight")

# Returns complete result with:
# - Orchestration plan
# - Agent responses
# - Quality reflection
# - Final synthesized response
# - Updated memory
```

## 📝 Prompts

All agent prompts are defined in [prompts.py](prompts.py) using Jinja2 templates. The prompts are based on the research paper's appendices and include:

- **DS Agent**: Statistical analysis planning and code generation
- **DE Agent**: Medical knowledge integration and synthesis
- **HC Agent**: Motivational interviewing and behavior change
- **Orchestrator**: Need understanding, reflection, and memory management

To customize prompts, edit the templates in [prompts.py](prompts.py).

## 🧪 Sample Queries

The system includes 8 sample health queries covering:
- Sleep quality analysis
- Cardiovascular health assessment
- Diabetes risk evaluation
- Fatigue investigation
- Exercise planning
- Lab result interpretation
- Weight loss coaching
- Stress level analysis (HRV)

## 🔬 Development

### Adding New Features

1. **New Agent Capabilities**: Add methods to agent classes in [agents.py](agents.py)
2. **New Prompts**: Add templates to [prompts.py](prompts.py)
3. **New Data Sources**: Extend mock data in [mock_data.py](mock_data.py)
4. **New Orchestration Logic**: Modify [orchestrator.py](orchestrator.py)

### Testing Individual Components

```bash
# Test API client
python api_client.py

# View mock data
python mock_data.py

# Test agents (add test code to agents.py)
python agents.py
```

## 🔒 Privacy & Safety

**Important Notes:**
- This is a research/demo system using mock data
- NOT intended for actual medical diagnosis or treatment
- Always encourages users to consult healthcare professionals
- Does not store real personal health information

## 📚 Research Paper

This implementation is based on:

**"The Anatomy of a Personal Health Agent"**
arXiv:2508.20148
[https://arxiv.org/abs/2508.20148](https://arxiv.org/abs/2508.20148)

The paper describes a multi-agent architecture for personalized health insights using LLMs with specialized roles for data analysis, medical expertise, and health coaching.

## 🛠️ Technology Stack

- **Python 3.8+**
- **Google Gemini API** (gemini-1.5-pro) - LLM backend
- **Jinja2** - Prompt templating
- **Mock Time-Series Data** - Simulated wearable device data

## 📄 License

[Specify your license here]

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Integration with real wearable device APIs (Fitbit, Apple Health, etc.)
- Enhanced statistical analysis methods
- Additional coaching strategies
- Support for more health data types
- Multi-language support

## 📧 Contact

[Your contact information]

---

**Disclaimer**: This system is for research and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.
