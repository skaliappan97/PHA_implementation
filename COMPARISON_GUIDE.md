# Multi-Agent vs Single-Agent Comparison Guide

This guide explains how to use the newly implemented single-agent baseline and comparison modes to evaluate the multi-agent architecture.

## Overview

The Personal Health Agent system now supports three operational modes for research and comparison:

1. **Multi-Agent Mode** (original) - DS, DE, and HC agents coordinated by an orchestrator
2. **Single-Agent Mode** (new) - Unified agent combining all DS/DE/HC capabilities
3. **Comparison Mode** (new) - Side-by-side comparison of both architectures

## Architecture Comparison

### Multi-Agent System
```
User Query
    ↓
Orchestrator (Step 1: Understand user need)
    ↓
Agent Selection & Task Assignment
    ↓
Parallel Agent Execution (DS, DE, HC)
    ↓
Response Synthesis
    ↓
Reflection & Quality Check
    ↓
Memory Update
    ↓
Final Response

LLM Calls: 5-7 per query
- 1 for understanding
- 1 for task assignment
- 1-3 for agents (DS, DE, HC)
- 1 for reflection
- 1 for memory update
```

### Single-Agent System
```
User Query
    ↓
Unified Agent (DS + DE + HC capabilities)
    ↓
Direct Processing
    ↓
Memory Update
    ↓
Final Response

LLM Calls: 2 per query
- 1 for processing
- 1 for memory update
```

## Usage

### Prerequisites

```bash
# Activate virtual environment
source .venv/bin/activate

# Ensure API key is set
export GOOGLE_API_KEY='your-gemini-api-key-here'
```

### 1. Single-Agent Interactive Mode

Run the single unified agent in interactive conversation mode:

```bash
python main.py single
```

**Commands:**
- Type your health queries naturally
- `memory` - View current memory state
- `summary` - Show conversation statistics
- `quit` - Exit

**Example Session:**
```
You: How has my sleep been over the past month?
PHA: Based on your data over the last 30 days...

You: What should I do to improve it?
PHA: Given your sleep patterns and constraints...

You: memory
{
  "goals": ["Improve sleep quality"],
  "key_metrics": ["sleep_hours", "sleep_quality_score"],
  ...
}
```

### 2. Comparison Mode

Compare both systems on a single query:

```bash
# Use a default sample query
python main.py compare

# Use a custom query
python main.py compare "Analyze my heart rate trends over the past month"
```

**Output Includes:**
- Both systems' responses
- Response time comparison
- LLM call estimates
- Success status
- Performance metrics

**Example Output:**
```
================================================================================
MULTI-AGENT SYSTEM
────────────────────────────────────────────────────────────────────────────
[Response from multi-agent system...]

⏱  Time: 8.45s
🤖 Main Agent: DS
🔗 Supporting: DE, HC

────────────────────────────────────────────────────────────────────────────
SINGLE-AGENT SYSTEM
────────────────────────────────────────────────────────────────────────────
[Response from single-agent system...]

⏱  Time: 3.21s
🤖 Agent: Unified (DS + DE + HC)

================================================================================
COMPARISON METRICS
================================================================================
⏱  Response Time:
   Multi-Agent: 8.45s
   Single-Agent: 3.21s
   Multi is 163.2% slower

📊 Estimated LLM Calls:
   Multi-Agent: 5-7 calls
   Single-Agent: 2 calls

🎯 Success Rate:
   Multi-Agent: ✓
   Single-Agent: ✓
```

### 3. Batch Comparison

Run multiple queries through both systems for comprehensive testing:

```bash
# Run all sample queries
python comparison.py --batch

# Run a custom query
python comparison.py --query "Help me create an exercise plan"
```

**Batch Output Includes:**
- Individual query comparisons
- Aggregate statistics:
  - Average response times
  - Success rates
  - Total LLM call estimates
- Results saved to JSON file for further analysis

**Example Batch Summary:**
```
================================================================================
BATCH COMPARISON SUMMARY
================================================================================
📊 Total Queries: 8

⏱  Average Response Time:
   Multi-Agent:  7.83s
   Single-Agent: 3.14s

🎯 Success Rate:
   Multi-Agent:  100.0%
   Single-Agent: 100.0%

📞 Estimated Total LLM Calls:
   Multi-Agent:  ~48 calls
   Single-Agent: ~16 calls
   Reduction:    66.7% fewer calls with single-agent

💾 Results saved to: comparison_results_1729012345.json
```

## Comparison Framework API

For programmatic testing, use the `AgentComparison` class:

```python
from comparison import AgentComparison
from mock_data import get_mock_user_data

# Initialize
user_data = get_mock_user_data()
comparison = AgentComparison(user_data)

# Single query
result = comparison.run_single_query_comparison("How has my sleep been?")

# Multiple queries
queries = [
    "Analyze my heart rate trends",
    "What should I know about my cholesterol?",
    "Help me lose 10 pounds"
]
report = comparison.run_batch_comparison(queries, save_results=True)

# Access metrics
print(f"Multi-agent avg time: {report['avg_response_time']['multi_agent']:.2f}s")
print(f"Single-agent avg time: {report['avg_response_time']['single_agent']:.2f}s")
```

## Evaluation Criteria

### Quantitative Metrics

1. **Response Time**
   - Wall-clock time from query to response
   - Lower is better
   - Expected: Single-agent faster due to fewer LLM calls

2. **LLM Call Count**
   - Number of API calls per query
   - Lower is better (cost and latency)
   - Expected: Single-agent ~2 calls vs multi-agent ~6 calls

3. **Success Rate**
   - Percentage of queries successfully processed
   - Higher is better
   - Expected: Both should be high (>95%)

### Qualitative Metrics (Manual Evaluation)

1. **Response Quality**
   - Depth of analysis
   - Medical accuracy
   - Actionability of recommendations
   - Expected: Multi-agent may provide more structured responses

2. **Response Coherence**
   - Integration of different expertise domains
   - Consistency across conversation turns
   - Expected: Multi-agent may have better domain specialization

3. **Memory Accuracy**
   - Correct extraction of goals, conditions, actions
   - Contextual awareness in follow-ups
   - Expected: Multi-agent may have advantage due to reflection step

4. **Conversation Flow**
   - Natural dialogue progression
   - Appropriate coaching techniques
   - Expected: Comparable between both systems

## Research Questions to Explore

1. **When does multi-agent architecture provide value?**
   - Complex queries requiring multiple perspectives?
   - Data analysis + medical interpretation + coaching?
   - Multi-turn conversations with evolving goals?

2. **What are the trade-offs?**
   - Response quality vs response time
   - Specialization vs generalization
   - Cost (LLM calls) vs performance

3. **Does orchestration overhead pay off?**
   - Is the reflection step worth the extra call?
   - Does agent specialization improve accuracy?
   - Is memory extraction more accurate with structured process?

4. **Edge cases and failure modes**
   - Which system handles ambiguous queries better?
   - How do they recover from errors?
   - Which maintains better conversation context?

## Tips for Effective Comparison

1. **Use diverse query types:**
   - Data-heavy: "Analyze my sleep patterns"
   - Medical knowledge: "What does my cholesterol mean?"
   - Coaching: "Help me stick to an exercise plan"
   - Mixed: "Based on my data, what health risks should I address?"

2. **Test multi-turn conversations:**
   - Start both systems fresh
   - Ask follow-up questions
   - Observe memory and context handling

3. **Document subjective observations:**
   - Which response was more helpful?
   - Which felt more natural?
   - Which gave more actionable advice?

4. **Compare on realistic use cases:**
   - Use actual health queries you'd ask
   - Test edge cases and unusual requests
   - Evaluate both systems on same criteria

## File Structure

```
gpha/
├── unified_agent.py           # NEW - Single unified agent
├── comparison.py              # NEW - Comparison framework
├── prompts.py                 # UPDATED - Added UNIFIED_AGENT_PROMPT
├── main.py                    # UPDATED - Added single & compare modes
├── test_single_agent.py       # NEW - Structure validation tests
├── COMPARISON_GUIDE.md        # NEW - This guide
├── orchestrator.py            # EXISTING - Multi-agent orchestrator
├── agents.py                  # EXISTING - DS, DE, HC agents
├── mock_data.py               # EXISTING - Test data
└── api_client.py              # EXISTING - Gemini API wrapper
```

## Next Steps

1. **Run initial comparisons:**
   ```bash
   python main.py compare "How has my sleep been?"
   python comparison.py --batch
   ```

2. **Analyze results:**
   - Review response quality
   - Compare metrics
   - Identify patterns

3. **Iterate and test:**
   - Try different query types
   - Test with real user data (when available)
   - Document findings

4. **Consider hybrid approaches:**
   - Could we combine benefits of both?
   - When to use which architecture?
   - Dynamic routing based on query complexity?

## Troubleshooting

**Error: ModuleNotFoundError: No module named 'google.generativeai'**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Error: API key not set**
```bash
export GOOGLE_API_KEY='your-key-here'
```

**Comparison takes too long**
- Use shorter queries for quick tests
- Test single queries before batch mode
- Consider using subset of sample queries

**Memory usage issues**
- Comparison results can be large
- Clear old comparison JSON files periodically
- Use `--no-save` flag if added in future

## Additional Resources

- Original paper: arXiv 2508.20148 "The Anatomy of a Personal Health Agent"
- Multi-agent documentation: [README.md](README.md)
- Project instructions: [CLAUDE.md](CLAUDE.md)

---

Happy comparing! This framework should help you determine whether the multi-agent orchestration provides meaningful benefits over a simpler unified agent approach.
