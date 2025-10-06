# Quick Reference Guide

**Personal Health Agent (PHA) - Multi-Agent System**

---

## ⚡ Quick Start (30 seconds)

```bash
# 1. Navigate to project
cd /Users/skaliappan/Documents/gpha

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Set API key (if not already set)
export GOOGLE_API_KEY='your-gemini-api-key'

# 4. Run demo
python main.py
```

---

## 🎯 Common Commands

| Command | Purpose |
|---------|---------|
| `python api_client.py` | Test Gemini API connection |
| `python mock_data.py` | View mock health data |
| `python main.py` | Run demo (2 sample queries) |
| `python main.py interactive` | Start conversation mode |
| `python main.py batch` | Run all 8 sample queries |
| `python main.py single "query"` | Run custom query |
| `python main.py data` | View data summary only |

---

## 📁 File Reference

| File | Purpose | Key Functions |
|------|---------|---------------|
| **api_client.py** | Gemini API wrapper | `call_gemini()` |
| **prompts.py** | Jinja2 templates | `render_prompt()`, `get_agent_prompt()` |
| **agents.py** | Three agent classes | `DataScienceAgent`, `DomainExpertAgent`, `HealthCoachAgent` |
| **orchestrator.py** | Multi-agent coordinator | `Orchestrator.process_query()` |
| **mock_data.py** | Health data simulation | `get_mock_user_data()`, `get_sample_queries()` |
| **main.py** | Entry point | `initialize_system()`, `run_interactive_mode()` |

---

## 🤖 Agent Quick Reference

### Data Science Agent
```python
from agents import DataScienceAgent

ds_agent = DataScienceAgent(personal_data={...})

# Two-stage analysis
result = ds_agent.analyze_query("How has my sleep changed?")
# Returns: {'analysis_plan': ..., 'analysis_code': ...}
```

### Domain Expert Agent
```python
from agents import DomainExpertAgent

de_agent = DomainExpertAgent(user_health_context={...})

# Answer health question
answer = de_agent.answer_health_question(
    "What does my cholesterol mean?",
    wearable_data={...}
)
```

### Health Coach Agent
```python
from agents import HealthCoachAgent

hc_agent = HealthCoachAgent(user_context={...})

# Identify goals
response = hc_agent.identify_goals(
    "I want to get healthier",
    health_insights={...}
)
```

---

## 🎛️ Orchestrator Usage

```python
from orchestrator import Orchestrator
from agents import DataScienceAgent, DomainExpertAgent, HealthCoachAgent

# Initialize agents
ds = DataScienceAgent(personal_data={...})
de = DomainExpertAgent(user_health_context={...})
hc = HealthCoachAgent(user_context={...})

# Create orchestrator
orchestrator = Orchestrator(ds, de, hc)

# Process query (runs 4-step process)
result = orchestrator.process_query("How has my sleep been?")

# Result contains:
# - orchestration_plan
# - agent_responses
# - reflection
# - response (final answer)
# - updated_memory
```

---

## 📊 Mock Data Structure

```python
from mock_data import get_mock_user_data

data = get_mock_user_data()

# Data structure:
{
    'user_profile': {
        'age': 35,
        'gender': 'male',
        'height_cm': 178,
        'weight_kg': 82,
        ...
    },
    'health_context': {
        'health_profile': {...},
        'health_records': {
            'conditions': [...],
            'medications': [...],
            'allergies': [...],
            ...
        },
        'wearable_data': {...}
    },
    'personal_data': {
        'wearable_data': {
            'heart_rate': [...],  # 720 data points
            'sleep': [...],        # 30 nights
            'activity': [...],     # 30 days
            'heart_rate_variability': [...]
        },
        ...
    },
    'lab_results': {...}
}
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
export GOOGLE_API_KEY='your-api-key'

# Optional (for future use)
export PHA_DEBUG=true
export PHA_LOG_LEVEL=INFO
```

### API Settings
```python
# In api_client.py
call_gemini(
    system_prompt="...",
    user_prompt="...",
    model="gemini-1.5-pro",      # Default model
    temperature=0.5,              # 0.0-1.0
    max_tokens=8192               # Max response length
)
```

---

## 🎨 Prompt Customization

### Using Templates
```python
from prompts import render_prompt, DS_ANALYSIS_PLAN_PROMPT

# Render a template
prompt = render_prompt(
    DS_ANALYSIS_PLAN_PROMPT,
    user_query="How has my sleep been?",
    data_summary="30 days of sleep data available"
)
```

### Temperature Guide
```python
# Code generation (very structured)
temperature = 0.2

# Analysis planning (structured but creative)
temperature = 0.3

# Medical advice (balanced)
temperature = 0.4-0.5

# Conversation (natural, conversational)
temperature = 0.6-0.7
```

---

## 📝 Sample Queries

1. "How has my sleep quality been over the past month?"
2. "I want to improve my cardiovascular health. What do my heart rate and activity data suggest?"
3. "My father has Type 2 diabetes. Based on my data, what's my risk?"
4. "I've been feeling more tired lately. Can you analyze my recent health data?"
5. "Help me create a realistic exercise plan."
6. "What does my recent lab work say about my cholesterol?"
7. "I want to lose 10 pounds over the next 3 months."
8. "How does my heart rate variability compare to healthy ranges?"

---

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if set
echo $GOOGLE_API_KEY

# Set temporarily
export GOOGLE_API_KEY='your-key'

# Set permanently (add to ~/.zshrc or ~/.bashrc)
echo 'export GOOGLE_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### Import Errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check installation
pip list | grep google-generativeai
```

### Runtime Errors
```python
# Enable detailed error messages
python -v main.py

# Test API client independently
python api_client.py

# Test data generation
python mock_data.py
```

---

## 📚 Interactive Mode Commands

While in interactive mode (`python main.py interactive`):

| Command | Action |
|---------|--------|
| Type your query | Ask health question |
| `memory` | View current conversation memory |
| `summary` | View conversation statistics |
| `quit` or `exit` | Exit interactive mode |

---

## 🔄 Workflow Examples

### Testing a New Feature
```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Edit the code
# (make changes to agents.py, prompts.py, etc.)

# 3. Test single query
python main.py single "test query"

# 4. If successful, test in batch
python main.py batch
```

### Adding a New Prompt
```python
# 1. Edit prompts.py
NEW_PROMPT = Template("""
Your new prompt here with {{ variables }}
""")

# 2. Use in agent
prompt = render_prompt(NEW_PROMPT, variables="values")
response = call_gemini(system_prompt, prompt)
```

### Creating a New Agent Method
```python
# In agents.py
class HealthCoachAgent:
    def new_method(self, user_input: str) -> str:
        """New capability description."""
        user_prompt = render_prompt(
            SOME_TEMPLATE,
            user_input=user_input
        )
        return call_gemini(self.system_prompt, user_prompt)
```

---

## 📖 Documentation Index

| Document | Purpose |
|----------|---------|
| **README.md** | General overview, quick start |
| **SETUP.md** | Installation and configuration |
| **CLAUDE.md** | Technical documentation |
| **ARCHITECTURE.md** | System architecture diagrams |
| **IMPLEMENTATION_SUMMARY.md** | What was built |
| **PROJECT_STATUS.md** | Completion checklist |
| **QUICK_REFERENCE.md** | This guide |

---

## 🚀 Getting Help

1. **Check Documentation**
   - Start with [README.md](README.md)
   - For setup issues: [SETUP.md](SETUP.md)
   - For technical details: [CLAUDE.md](CLAUDE.md)

2. **Test Components**
   ```bash
   python api_client.py      # Test API
   python mock_data.py       # Test data
   python main.py data       # View data
   ```

3. **Common Issues**
   - API key not set → See "API Key Issues" above
   - Import errors → Reinstall dependencies
   - Unexpected output → Check temperature settings

---

## ⚙️ Advanced Usage

### Programmatic Usage
```python
# Import the system
from main import initialize_system
from mock_data import get_sample_queries

# Initialize
orchestrator, user_data = initialize_system()

# Process queries programmatically
for query in get_sample_queries():
    result = orchestrator.process_query(query)
    print(result['response'])
```

### Custom Data
```python
# Replace mock data with custom data
custom_data = {
    'user_profile': {...},
    'health_context': {...},
    'personal_data': {...},
}

from agents import DataScienceAgent, DomainExpertAgent, HealthCoachAgent
ds = DataScienceAgent(custom_data['personal_data'])
de = DomainExpertAgent(custom_data['health_context'])
hc = HealthCoachAgent(custom_data['user_profile'])
```

---

## 💡 Tips & Best Practices

1. **Always activate virtual environment first**
2. **Set API key before running**
3. **Start with `python main.py data` to see mock data**
4. **Use interactive mode for exploration**
5. **Check memory after conversations to see what's tracked**
6. **Adjust temperature for different response styles**
7. **Read error messages carefully - they're informative**

---

## 📋 Checklist for First Run

- [ ] Virtual environment activated (`source .venv/bin/activate`)
- [ ] API key set (`export GOOGLE_API_KEY='...'`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API test successful (`python api_client.py`)
- [ ] Demo runs successfully (`python main.py`)

---

**Ready to go! Start with:** `python main.py`
