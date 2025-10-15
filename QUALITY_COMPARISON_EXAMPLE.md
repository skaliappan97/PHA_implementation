# Quality-Focused Comparison Output Example

This document shows what the new side-by-side comparison output looks like.

## New Format (Quality-Focused)

```
================================================================================================================================================================
RESPONSE QUALITY COMPARISON
================================================================================================================================================================

Query: How has my sleep quality been over the past month? Are there any patterns I should be aware of?

                              MULTI-AGENT SYSTEM                              │                             SINGLE-AGENT SYSTEM
────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────
Based on analysis of your 30-day sleep data, your average sleep duration    │ Looking at your sleep data over the past month, you're averaging 7.2
is 7.2 hours per night, which falls within the recommended 7-9 hour range   │ hours per night, which is within the healthy range. However, I notice
for adults. However, I've identified several important patterns that         │ some variability - your sleep quality score averages 78.5/100, with
warrant attention. Your sleep quality score averages 78.5 out of 100,        │ considerable fluctuation between 62-94. You're waking up 2-3 times per
indicating moderate quality with room for improvement. Deep sleep accounts   │ night on average. Your deep sleep (1.5 hours) and REM sleep (1.8 hours)
for approximately 1.5 hours per night (21% of total), which is slightly     │ are slightly below optimal levels. I'd recommend establishing a more
below the optimal 20-25% range. REM sleep averages 1.8 hours (25%),         │ consistent bedtime routine and avoiding screens 1 hour before sleep to
which is within normal parameters. Your sleep consistency shows              │ improve both duration and quality. Would you like to discuss specific
weekday/weekend variation, with later bedtimes on weekends potentially       │ strategies to reduce those nighttime awakenings?
disrupting your circadian rhythm. The data indicates you wake 2-3 times      │
per night on average, which could be contributing to the suboptimal deep     │
sleep percentage. From a clinical perspective, improving sleep consistency   │
and addressing fragmentation should be priorities. I recommend               │
establishing a fixed sleep schedule, optimizing your sleep environment       │
(temperature 65-68°F, darkness, quiet), and avoiding screens 60 minutes      │
before bed. Given your family history of hypertension and current            │
pre-hypertension status, quality sleep is particularly important for         │
cardiovascular health management. Would you like me to help you develop a    │
structured sleep improvement plan?                                           │
────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────

================================================================================================================================================================

Compare the responses above based on:
  • Depth and thoroughness of analysis
  • Medical accuracy and clinical reasoning
  • Actionability and practical recommendations
  • Personalization to user's specific context
  • Clarity and helpfulness of explanation

================================================================================================================================================================
```

## Key Improvements

### 1. **Side-by-Side Layout**
- Both responses visible simultaneously
- Easy to compare length, depth, and approach
- No scrolling required to compare

### 2. **Quality-First Focus**
- **No timing metrics by default** (adds `--metrics` flag if you want them)
- Emphasizes response content over performance
- Evaluation criteria clearly listed

### 3. **Evaluation Prompts**
After each comparison, you're prompted to evaluate based on:
- **Depth and thoroughness**: Which provides more comprehensive analysis?
- **Medical accuracy**: Which demonstrates better clinical reasoning?
- **Actionability**: Which gives more practical, actionable advice?
- **Personalization**: Which better tailors to user's specific context?
- **Clarity**: Which is easier to understand and more helpful?

### 4. **Optional Metrics**
If you want to see timing/API metrics, use the `--metrics` flag:

```bash
python main.py compare "query" --metrics
python comparison.py --batch --metrics
```

With `--metrics`, you'll see:
```
⏱  Response Time: Multi=8.45s | Single=3.21s
📞 LLM Calls: Multi=5-7 | Single=2
```

## Usage Examples

### Single Query Comparison (Quality Focus)
```bash
# Default: Quality comparison only
python main.py compare "How has my sleep been?"

# With metrics if you want timing data
python main.py compare "How has my sleep been?" --metrics
```

### Batch Comparison
```bash
# Compare all sample queries with quality focus
python comparison.py --batch

# Compare with timing metrics
python comparison.py --batch --metrics

# Custom query
python comparison.py --query "Help me improve my cardiovascular health"
```

### Interactive Batch Mode
When running `--batch`, the system will:
1. Show Query 1 comparison (both responses side-by-side)
2. Wait for you to evaluate
3. Press Enter → shows Query 2
4. Repeat for all queries

This gives you time to carefully evaluate each comparison before moving on.

## Benefits

✅ **Easier Evaluation**: See both responses at once, no context switching
✅ **Quality-Focused**: Emphasizes content over speed/cost
✅ **Clear Criteria**: Evaluation dimensions explicitly listed
✅ **Flexible**: Add `--metrics` if you want performance data
✅ **Paced Review**: Batch mode pauses between queries for careful evaluation
✅ **Clean Output**: No clutter, just the information needed for quality comparison

## Comparing Dimensions

### When Multi-Agent Might Excel
- More structured analysis (separate DS/DE/HC perspectives)
- Deeper domain integration
- More thorough medical context
- Reflection step catches issues

### When Single-Agent Might Excel
- More conversational and natural
- Better flow without orchestration overhead
- More direct and concise
- Faster to insights

### What to Look For

**Depth**: Does one provide more statistical detail? More medical background?

**Integration**: Does one better connect wearable data + medical records + coaching?

**Actionability**: Does one provide more concrete, feasible recommendations?

**Personalization**: Does one better account for user's specific context (age, conditions, constraints)?

**Clarity**: Is one easier to understand? More helpful? Better formatted?

## Terminal Width Note

The side-by-side display is optimized for **160-character wide terminals**.

If your terminal is narrower, responses may wrap. You can:
- Expand your terminal window
- Or the wrapping will still be readable, just less elegant

---

Now you can focus purely on **which agent provides better responses** rather than getting distracted by timing metrics!
