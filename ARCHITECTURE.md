# System Architecture: Personal Health Agent (PHA)

This document provides detailed architectural diagrams and flow charts for the PHA multi-agent system.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                            USER                                      │
│                    (Health Queries & Feedback)                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         MAIN.PY                                      │
│                    (Entry Point & Demo Modes)                        │
│  ┌─────────────┬──────────────┬──────────────┬─────────────────┐   │
│  │   Demo      │ Interactive  │   Batch      │  Single Query   │   │
│  │   Mode      │    Mode      │   Mode       │     Mode        │   │
│  └─────────────┴──────────────┴──────────────┴─────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                    │
│                  (4-Step Coordination Process)                       │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STEP 1: Understand User Need                              │    │
│  │  • Analyze query intent                                    │    │
│  │  • Determine required agents (DS, DE, HC)                  │    │
│  │  • Assign main agent and supporting agents                 │    │
│  └────────────────────────────────────────────────────────────┘    │
│                            ▼                                         │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STEP 2: Orchestrate Agents                                │    │
│  │  • Route tasks to selected agents                          │    │
│  │  • Collect responses                                       │    │
│  │  • Pass supporting agent outputs to main agent             │    │
│  └────────────────────────────────────────────────────────────┘    │
│                            ▼                                         │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STEP 3: Reflect on Response                               │    │
│  │  • Check completeness                                      │    │
│  │  • Validate coherence                                      │    │
│  │  • Assess safety                                           │    │
│  │  • Improve if needed                                       │    │
│  └────────────────────────────────────────────────────────────┘    │
│                            ▼                                         │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  STEP 4: Update Memory                                     │    │
│  │  • Extract entities (goals, conditions, etc.)              │    │
│  │  • Update conversation history                             │    │
│  │  • Log action items                                        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────┬────────────────┬────────────────┬───────────────────────────┘
      │                │                │
      ▼                ▼                ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ DS Agent │    │ DE Agent │    │ HC Agent │
│          │    │          │    │          │
│ Analysis │    │ Medical  │    │ Coaching │
│ & Stats  │    │Knowledge │    │ & Goals  │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     └───────────────┴───────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   API_CLIENT.PY       │
         │   (Gemini API Wrapper)│
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Google Gemini API   │
         │   (gemini-1.5-pro)    │
         └───────────────────────┘
```

---

## 🔄 Query Processing Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│ 1. ORCHESTRATOR: Understand Need            │
│                                             │
│ Input: "How has my sleep been this month?"  │
│                                             │
│ Analysis:                                   │
│  • Intent: Sleep quality analysis           │
│  • Main Agent: DS (data analysis needed)    │
│  • Supporting: DE (medical context),        │
│                HC (recommendations)         │
│                                             │
│ Output: Orchestration Plan (JSON)           │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ 2. ORCHESTRATOR: Route to Agents            │
│                                             │
│ DS Agent Task:                              │
│  → generate_analysis_plan()                 │
│  → analyze_query()                          │
│  → Returns: Statistical analysis            │
│                                             │
│ DE Agent Task:                              │
│  → synthesize_insights()                    │
│  → Input: DS analysis + health records      │
│  → Returns: Medical interpretation          │
│                                             │
│ HC Agent Task:                              │
│  → provide_recommendations()                │
│  → Input: DS + DE insights                  │
│  → Returns: Personalized coaching           │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ 3. ORCHESTRATOR: Reflect                    │
│                                             │
│ Quality Checks:                             │
│  ✓ Completeness: Addresses user query?     │
│  ✓ Coherence: Agents align?                │
│  ✓ Accuracy: No contradictions?            │
│  ✓ Actionability: Clear recommendations?   │
│  ✓ Safety: Flags medical concerns?         │
│                                             │
│ Result: APPROVED ✓                          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ 4. ORCHESTRATOR: Update Memory              │
│                                             │
│ Extract & Log:                              │
│  • Goals: "Improve sleep quality"           │
│  • Metrics: "Sleep avg 7.2 hrs"             │
│  • Action Items: "Track caffeine intake"    │
│  • Progress: "Monitoring sleep patterns"    │
│                                             │
│ Updated Memory → Next Query Context         │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
              Final Response
                   │
                   ▼
                 USER
```

---

## 🤖 Agent Interaction Patterns

### Pattern 1: DS as Main Agent (Data Analysis Query)

```
User: "What's the trend in my heart rate over the past week?"

Orchestrator
    │
    ├── Main: DS Agent
    │   ├── generate_analysis_plan()
    │   │   └── Creates statistical analysis strategy
    │   ├── generate_analysis_code()
    │   │   └── Generates Python code for analysis
    │   └── Returns: Analysis plan + code
    │
    ├── Supporting: DE Agent
    │   ├── synthesize_insights()
    │   │   └── Adds medical context to trends
    │   └── Returns: Medical interpretation
    │
    └── Supporting: HC Agent
        └── provide_recommendations()
            └── Returns: "Based on your HR trend..."
```

### Pattern 2: DE as Main Agent (Medical Question)

```
User: "What does my cholesterol level mean for my health?"

Orchestrator
    │
    ├── Main: DE Agent
    │   ├── answer_health_question()
    │   │   └── Medical knowledge about cholesterol
    │   ├── synthesize_insights()
    │   │   └── Lab results + family history
    │   └── Returns: Comprehensive medical answer
    │
    ├── Supporting: DS Agent
    │   └── analyze_query()
    │       └── Returns: Statistical comparison to norms
    │
    └── Supporting: HC Agent
        └── provide_recommendations()
            └── Returns: Lifestyle recommendations
```

### Pattern 3: HC as Main Agent (Goal Setting)

```
User: "I want to lose weight and get healthier."

Orchestrator
    │
    ├── Main: HC Agent
    │   ├── identify_goals()
    │   │   └── Motivational interviewing
    │   ├── provide_recommendations()
    │   │   └── Personalized action plan
    │   └── Returns: Coaching dialogue
    │
    ├── Supporting: DS Agent
    │   └── analyze_query()
    │       └── Returns: Current activity/weight trends
    │
    └── Supporting: DE Agent
        └── synthesize_insights()
            └── Returns: Health considerations for weight loss
```

---

## 📊 Data Flow Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    MOCK_DATA.PY                          │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  User Profile                                   │    │
│  │  • Age, gender, height, weight, BMI            │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Health Context                                 │    │
│  │  • Conditions: Pre-hypertension                 │    │
│  │  • Medications: Vitamin D                       │    │
│  │  • Allergies, Family history                    │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Wearable Data (30 days)                        │    │
│  │  • Heart Rate: 720 measurements                 │    │
│  │  • Sleep: 30 nights of data                     │    │
│  │  • Activity: 30 days steps/calories             │    │
│  │  • HRV: 720 measurements                        │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Lab Results                                    │    │
│  │  • Cholesterol, Glucose, HbA1c, Vitamins        │    │
│  └────────────────────────────────────────────────┘    │
└───────────────────────┬──────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │  DS Agent    │        │  DE Agent    │
    │              │        │              │
    │ personal_data│        │health_context│
    └──────────────┘        └──────────────┘
                                    │
                                    ▼
                            ┌──────────────┐
                            │  HC Agent    │
                            │              │
                            │ user_profile │
                            └──────────────┘
```

---

## 🧠 Memory & Context Architecture

```
┌──────────────────────────────────────────────────────┐
│              ORCHESTRATOR MEMORY                      │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Goals                                        │    │
│  │ • ["Improve sleep quality",                 │    │
│  │   "Reduce stress levels"]                   │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Conditions                                   │    │
│  │ • ["Pre-hypertension"]                      │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Medications                                  │    │
│  │ • ["Vitamin D3"]                            │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Lifestyle                                    │    │
│  │ • {sleep_target: "8 hours",                 │    │
│  │    exercise_frequency: "3x/week"}           │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Key Metrics                                  │    │
│  │ • ["Avg sleep: 7.2 hrs",                    │    │
│  │   "Avg steps: 9500"]                        │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Action Items                                 │    │
│  │ • ["Track caffeine intake",                 │    │
│  │   "Schedule cardio checkup"]                │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ Conversation History                         │    │
│  │ • Turn 1: User + Assistant                  │    │
│  │ • Turn 2: User + Assistant                  │    │
│  │ • ... (Last 10 turns kept)                  │    │
│  └─────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
         │                                    ▲
         │ Used in every query                │
         ▼                                    │
┌────────────────────┐              ┌─────────────────┐
│  Prompt Context    │              │ Memory Update   │
│  Injection         │              │ (Step 4)        │
└────────────────────┘              └─────────────────┘
```

---

## 📝 Prompt Template System

```
┌──────────────────────────────────────────────────────────┐
│                     PROMPTS.PY                            │
│                (Jinja2 Template Library)                  │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │ System Prompts (Define Agent Identity)          │    │
│  │                                                  │    │
│  │ • DS_AGENT_PROMPT                               │    │
│  │   → "You are the Data Science Agent..."         │    │
│  │                                                  │    │
│  │ • DE_AGENT_PROMPT                               │    │
│  │   → "You are the Domain Expert Agent..."        │    │
│  │                                                  │    │
│  │ • HC_AGENT_PROMPT                               │    │
│  │   → "You are the Health Coach Agent..."         │    │
│  │                                                  │    │
│  │ • ORCHESTRATOR_SYSTEM_PROMPT                    │    │
│  │   → "You are the Orchestrator..."               │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Task-Specific Templates (Jinja2)                │    │
│  │                                                  │    │
│  │ DS Agent:                                        │    │
│  │ • DS_ANALYSIS_PLAN_PROMPT                       │    │
│  │ • DS_CODE_GENERATION_PROMPT                     │    │
│  │                                                  │    │
│  │ DE Agent:                                        │    │
│  │ • DE_HEALTH_QUESTION_PROMPT                     │    │
│  │ • DE_SYNTHESIS_PROMPT                           │    │
│  │                                                  │    │
│  │ HC Agent:                                        │    │
│  │ • HC_GOAL_IDENTIFICATION_PROMPT                 │    │
│  │ • HC_RECOMMENDATION_PROMPT                      │    │
│  │ • HC_FEEDBACK_PROCESSING_PROMPT                 │    │
│  │                                                  │    │
│  │ Orchestrator:                                    │    │
│  │ • ORCHESTRATOR_NEED_UNDERSTANDING_PROMPT        │    │
│  │ • ORCHESTRATOR_REFLECTION_PROMPT                │    │
│  │ • ORCHESTRATOR_MEMORY_UPDATE_PROMPT             │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Utility Functions                                │    │
│  │                                                  │    │
│  │ • render_prompt(template, **kwargs)             │    │
│  │   → Injects variables into Jinja2 template      │    │
│  │                                                  │    │
│  │ • get_agent_prompt(agent_type, **context)       │    │
│  │   → Returns rendered system prompt              │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │  call_gemini()  │
                  │  (API Client)   │
                  └─────────────────┘
```

---

## 🔌 API Integration Architecture

```
┌────────────────────────────────────────────┐
│              AGENTS & ORCHESTRATOR          │
│                                             │
│  All components call:                       │
│  call_gemini(system_prompt, user_prompt)    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          API_CLIENT.PY                       │
│                                             │
│  call_gemini():                             │
│  1. Load GOOGLE_API_KEY from env           │
│  2. Initialize GenerativeModel              │
│  3. Combine system + user prompts           │
│  4. Call Gemini API                         │
│  5. Extract response text                   │
│  6. Handle errors gracefully                │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│      google.generativeai Library            │
│                                             │
│  • genai.configure(api_key=...)            │
│  • genai.GenerativeModel(...)              │
│  • model.generate_content(...)             │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ Google Gemini API   │
         │  (gemini-1.5-pro)   │
         └─────────────────────┘
```

---

## 🎯 Agent Decision Logic

```
Query: "How has my sleep been this month?"
           │
           ▼
┌──────────────────────────────────────────────┐
│ ORCHESTRATOR: Analyze Query Type             │
│                                              │
│ Intent Detection:                            │
│  • Keywords: "sleep", "month", "trend"       │
│  • Type: Analytical + Informational          │
│                                              │
│ Agent Selection Logic:                       │
│  IF (query needs data analysis)              │
│     → Main: DS Agent                         │
│  IF (query needs medical knowledge)          │
│     → Supporting: DE Agent                   │
│  IF (query implies goals/coaching)           │
│     → Supporting: HC Agent                   │
│                                              │
│ Decision:                                    │
│  Main: DS (needs sleep data analysis)        │
│  Supporting: DE (medical context on sleep)   │
│  Supporting: HC (sleep improvement tips)     │
└──────────────────────────────────────────────┘
```

---

## 📈 Scalability Considerations

### Current Architecture (Single User, In-Memory)
```
User → Main.py → Orchestrator → Agents → Gemini API
                      ↓
                  Memory (RAM)
```

### Future Production Architecture
```
Multiple Users → Web API → Load Balancer
                              ↓
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Orchestrator 1      Orchestrator 2
                    ↓                   ↓
              Agent Pool           Agent Pool
                    ↓                   ↓
              Gemini API          Gemini API
                    ↓
              PostgreSQL
              (User data, conversation history)
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────┐
│  Environment Variables               │
│  • GOOGLE_API_KEY (secure storage)  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  API Client (api_client.py)         │
│  • API key never logged             │
│  • Error messages sanitized         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Mock Data (mock_data.py)           │
│  • No real PHI (Protected Health    │
│    Information)                     │
│  • Simulated data only              │
└─────────────────────────────────────┘

Future Production Considerations:
• Encryption at rest (database)
• Encryption in transit (HTTPS/TLS)
• User authentication (OAuth 2.0)
• HIPAA compliance for real PHI
• Audit logging
• Data retention policies
```

---

## 📚 Summary

This architecture provides:
- ✅ **Modular Design**: Each component has clear responsibilities
- ✅ **Scalability**: Can be extended to multi-user, distributed systems
- ✅ **Flexibility**: Easy to add new agents or capabilities
- ✅ **Maintainability**: Well-documented with clear interfaces
- ✅ **Testability**: Components can be tested independently
- ✅ **Extensibility**: Plugin-based agent system

The current implementation is optimized for:
- Single-user scenarios
- Research and development
- Demonstration and testing
- Proof of concept validation

Future enhancements would focus on:
- Multi-user support
- Real-time data integration
- Web/mobile interfaces
- Production deployment
- Security hardening
