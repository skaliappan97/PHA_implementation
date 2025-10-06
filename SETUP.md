# Setup Guide for Personal Health Agent (PHA)

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation Steps

### 1. Clone and Navigate

```bash
cd /Users/skaliappan/Documents/gpha
```

### 2. Set Up Virtual Environment

The virtual environment is already created in `.venv/`. Activate it:

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key

You need to set your Google Gemini API key as an environment variable.

#### Option A: Temporary (current session only)

```bash
# macOS/Linux
export GOOGLE_API_KEY='your-api-key-here'

# Windows Command Prompt
set GOOGLE_API_KEY=your-api-key-here

# Windows PowerShell
$env:GOOGLE_API_KEY='your-api-key-here'
```

#### Option B: Permanent (recommended)

Add to your shell configuration file:

```bash
# For bash users (~/.bashrc or ~/.bash_profile)
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# For zsh users (~/.zshrc) - macOS default
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### Option C: Using .env file (not implemented yet, but you can add python-dotenv)

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your-api-key-here
```

## Verification

### Test 1: API Client

```bash
python api_client.py
```

Expected output:
```
✅ Gemini API client initialized successfully

Testing the Gemini API client...

--- Test Response ---
[Response from Gemini about API clients]
---------------------

✅ Test Successful! Your Gemini API client is ready to be used by your agents.
```

### Test 2: Mock Data

```bash
python mock_data.py
```

Expected output: Summary of user profile, health conditions, wearable data, and lab results.

### Test 3: Full System Demo

```bash
python main.py
```

Expected output: System initialization message, mock data summary, and processing of 2 sample queries.

## Troubleshooting

### Issue: "GOOGLE_API_KEY not found in environment variables"

**Solution**: Make sure you've set the environment variable correctly. After setting it, verify:

```bash
# macOS/Linux
echo $GOOGLE_API_KEY

# Windows Command Prompt
echo %GOOGLE_API_KEY%

# Windows PowerShell
echo $env:GOOGLE_API_KEY
```

### Issue: "Import 'google.generativeai' could not be resolved"

**Solution**: Make sure you've activated the virtual environment and installed dependencies:

```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: API errors or timeouts

**Solution**:
1. Check your internet connection
2. Verify your API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Check if you've exceeded API quota limits

### Issue: "ModuleNotFoundError"

**Solution**: Ensure you're in the virtual environment:

```bash
which python  # Should show .venv/bin/python
pip list      # Should show google-generativeai, jinja2, etc.
```

## Usage Examples

### Interactive Mode

Start a conversation with the PHA:

```bash
python main.py interactive
```

### Run All Sample Queries

```bash
python main.py batch
```

### Single Query

```bash
python main.py single "How has my sleep quality been this month?"
```

### View Data Only

```bash
python main.py data
```

## Next Steps

Once everything is working:

1. **Customize Prompts**: Edit templates in [prompts.py](prompts.py) to match the exact prompts from the research paper's appendices
2. **Add Real Data**: Replace mock data with connections to real wearable APIs (Fitbit, Apple Health, etc.)
3. **Extend Agents**: Add more capabilities to agents in [agents.py](agents.py)
4. **Improve Orchestration**: Enhance the orchestrator logic in [orchestrator.py](orchestrator.py)

## Development Workflow

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Make code changes

# 3. Test individual components
python api_client.py      # Test API
python mock_data.py       # Test data generation
python main.py single "test query"  # Test full system

# 4. Run comprehensive tests
python main.py batch      # Test all sample queries
```

## File Overview

- **api_client.py** - Gemini API wrapper
- **prompts.py** - Jinja2 prompt templates
- **agents.py** - DS, DE, HC agent implementations
- **orchestrator.py** - Multi-agent coordinator
- **mock_data.py** - Simulated health data
- **main.py** - Entry point and demo modes
- **requirements.txt** - Python dependencies
- **README.md** - Project documentation
- **CLAUDE.md** - Claude Code guidance
- **SETUP.md** - This file

## Support

For issues or questions:
1. Check the [README.md](README.md) for detailed documentation
2. Review the [CLAUDE.md](CLAUDE.md) for implementation details
3. Ensure you're following the exact setup steps above

## License

[Specify your license]
