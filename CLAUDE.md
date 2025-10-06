# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Personal Health Agent (PHA) multi-agent system based on the research paper (arXiv 2508.20148). The system uses three specialized AI agents that collaborate to provide personalized health insights and coaching:

1. **Data Science Agent** - Analyzes time-series wearable and health data, performs statistical analysis
2. **Domain Expert Agent** - Provides medical context and health interpretations
3. **Health Coach Agent** - Guides users toward health goals using motivational coaching strategies

## Architecture

The system follows a multi-agent orchestration pattern with four core components:

### Core Files

- **[api_client.py](api_client.py)** - Google Gemini API wrapper using `gemini-1.5-pro` model
  - `call_gemini(system_prompt, user_prompt, model, temperature, max_tokens)` - Main API interface
  - Handles API authentication via `GOOGLE_API_KEY` environment variable

- **[prompts.py](prompts.py)** - Jinja2-based prompt templates for all agents
  - `DS_AGENT_PROMPT` - Data Science Agent system prompt
  - `DE_AGENT_PROMPT` - Domain Expert Agent system prompt
  - `HC_AGENT_PROMPT` - Health Coach Agent system prompt
  - `ORCHESTRATOR_SYSTEM_PROMPT` - Orchestrator system prompt
  - Module-specific prompts for analysis planning, code generation, health questions, etc.
  - `get_agent_prompt(agent_type, **context)` - Get rendered system prompts
  - `render_prompt(template, **kwargs)` - Render Jinja2 templates with context

- **[agents.py](agents.py)** - Three specialized agent implementations
  - `DataScienceAgent` - Two-stage process: analysis plan → code generation
    - `generate_analysis_plan(user_query, data_summary)` - Create statistical analysis plan
    - `generate_analysis_code(analysis_plan, user_query)` - Generate Python code
    - `analyze_query(user_query)` - Complete two-stage analysis
  - `DomainExpertAgent` - Medical knowledge and health advice
    - `answer_health_question(user_question, wearable_data)` - Provide medical insights
    - `synthesize_insights(user_query, ds_analysis, lab_results)` - Integrate multiple data sources
  - `HealthCoachAgent` - Motivational coaching using MI techniques
    - `identify_goals(user_message, health_insights)` - Extract goals through dialogue
    - `provide_recommendations(user_goals, ds_insights, de_insights)` - Personalized advice
    - `handle_feedback(previous_recommendation, user_feedback)` - Adjust coaching approach
  - `create_agents(user_data)` - Factory function to initialize all agents

- **[orchestrator.py](orchestrator.py)** - Multi-agent coordination using 4-step process
  - `Orchestrator` class coordinates DS, DE, and HC agents
  - **Step 1**: `understand_user_need(user_query)` - Analyze query, determine needed agents
  - **Step 2**: `orchestrate_agents(user_query, plan)` - Route tasks to main/supporting agents
  - **Step 3**: `reflect_on_response(query, plan, responses, proposed)` - Quality check
  - **Step 4**: `update_memory(user_query, final_response)` - Log conversation entities
  - `process_query(user_query)` - Complete end-to-end query processing
  - Maintains conversation memory and context

- **[mock_data.py](mock_data.py)** - Simulated health data for testing
  - `generate_time_series()` - Create realistic wearable time-series data
  - `generate_sleep_data()` - Generate 30 days of sleep metrics
  - `generate_activity_data()` - Generate daily activity/step data
  - `MOCK_USER_DATA` - Complete user profile with health records, lab results, wearable data
  - `get_mock_user_data()` - Get all mock data for system initialization
  - `get_sample_queries()` - Get 8 sample health queries for testing

- **[main.py](main.py)** - Entry point with multiple execution modes
  - `initialize_system()` - Create agents and orchestrator with mock data
  - `run_single_query_demo(orchestrator, query)` - Process and display one query
  - `run_interactive_mode(orchestrator)` - Interactive conversation loop
  - `run_batch_demo(orchestrator, queries, num)` - Run multiple queries sequentially
  - Modes: demo, interactive, batch, single, data

## Environment Setup

### Required Environment Variables

```bash
export GOOGLE_API_KEY='your-gemini-api-key-here'
```

### Installation

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Project

### Quick Start

```bash
# Run demo mode (2 sample queries)
python main.py

# Test API client
python api_client.py

# View mock data
python mock_data.py
```

### Execution Modes

```bash
# Interactive conversation mode
python main.py interactive

# Run all sample queries
python main.py batch

# Single custom query
python main.py single "How has my sleep been?"

# View data summary only
python main.py data
```

## Key Implementation Notes

### Agent Design
- All agents use Google Gemini API (`gemini-1.5-pro`) via shared `call_gemini()` function
- Each agent has distinct system prompts and specialized methods
- Prompts use Jinja2 templates for dynamic context injection
- DS Agent implements two-stage process: plan generation → code generation
- DE Agent synthesizes insights from multiple data sources
- HC Agent uses motivational interviewing techniques

### Orchestrator Pattern
- Implements 4-step process from research paper:
  1. Understand user need → determine required agents
  2. Orchestrate agents → route tasks to main/supporting agents
  3. Reflect on response → quality check before user presentation
  4. Update memory → log entities for conversation context
- Maintains conversation history and memory (goals, conditions, medications, etc.)
- Dynamically assigns main/supporting agents based on query type
- Uses JSON parsing for structured communication between steps

### Data Architecture
- Mock data simulates 30 days of wearable device metrics
- Includes health records, lab results, user profile
- Time-series data for: heart rate, sleep, activity, HRV
- Realistic patterns (daily cycles, weekday/weekend variation)

### Prompt Engineering
- System prompts define agent roles and responsibilities
- User prompts constructed dynamically with Jinja2 templates
- Context includes: user data, conversation history, other agents' insights
- Temperature varies by task: lower for code (0.2), higher for conversation (0.7)

### Error Handling
- API errors gracefully handled in `call_gemini()`
- Agent errors captured in orchestration responses
- JSON parsing failures have fallback behaviors
- Interactive mode continues despite individual query errors

## Development Guidelines

### Adding New Agent Capabilities
1. Add method to appropriate agent class in [agents.py](agents.py)
2. Create corresponding Jinja2 prompt template in [prompts.py](prompts.py)
3. Update orchestrator logic in [orchestrator.py](orchestrator.py) if needed
4. Test with mock data

### Customizing Prompts
- Edit templates in [prompts.py](prompts.py)
- Use `{{ variable }}` syntax for dynamic content
- Test prompt changes with `render_prompt()` function
- Adjust temperature based on task (structured: 0.2-0.3, conversational: 0.6-0.7)

### Extending Mock Data
- Add new metrics to `MOCK_USER_DATA` in [mock_data.py](mock_data.py)
- Use `generate_time_series()` for time-series data
- Update agent initialization to include new data fields

### Testing Individual Components
```python
# Test API client
python api_client.py

# Test agents (add __main__ block to agents.py)
from agents import create_agents
from mock_data import get_mock_user_data
agents = create_agents(get_mock_user_data())

# Test orchestrator
from orchestrator import Orchestrator
orchestrator = Orchestrator(agents['ds'], agents['de'], agents['hc'])
```

## Project Structure

```
gpha/
├── .venv/              # Virtual environment
├── api_client.py       # Gemini API wrapper (✓ implemented)
├── prompts.py          # Jinja2 prompt templates (✓ implemented)
├── agents.py           # DS, DE, HC agent classes (✓ implemented)
├── orchestrator.py     # Multi-agent coordinator (✓ implemented)
├── mock_data.py        # Simulated health data (✓ implemented)
├── main.py            # Entry point + demos (✓ implemented)
├── requirements.txt    # Dependencies (✓ implemented)
├── README.md          # User documentation (✓ implemented)
└── CLAUDE.md          # This file (✓ updated)
```

## Dependencies

- `google-generativeai>=0.3.0` - Google Gemini API client
- `jinja2>=3.1.0` - Template engine for prompts
- `python-dotenv>=1.0.0` - Environment variable management

## Virtual Environment

Virtual environment located in `.venv/`

Activate with:
```bash
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```
