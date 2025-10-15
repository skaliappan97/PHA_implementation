"""
Unified Agent implementation for single-agent baseline comparison.

This module provides a single agent that combines all capabilities of the
Data Science, Domain Expert, and Health Coach agents into one unified system.
Used for comparing multi-agent vs single-agent architectures.
"""

from api_client import call_gemini
from prompts import UNIFIED_AGENT_PROMPT, UNIFIED_MEMORY_UPDATE_PROMPT, render_prompt
import json
from typing import Dict, Any, List


class UnifiedAgent:
    """
    Unified Health Agent that combines DS, DE, and HC capabilities.

    This agent handles all three domains in a single prompt:
    - Data analysis and statistics (DS capabilities)
    - Medical knowledge and interpretation (DE capabilities)
    - Health coaching and behavior change (HC capabilities)

    Used as a baseline to compare against the multi-agent system.
    """

    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize the Unified Agent with complete user data.

        Args:
            user_data: Complete user data including:
                - personal_data: Wearable and time-series data
                - health_context: Health records, conditions, medications
                - user_profile: Demographics and basic info
                - lab_results: Lab test results
        """
        self.user_data = user_data

        # Initialize memory structure (same as Orchestrator)
        self.memory = {
            'goals': [],
            'conditions': user_data.get('health_context', {}).get('health_records', {}).get('conditions', []),
            'lifestyle': {},
            'medications': user_data.get('health_context', {}).get('health_records', {}).get('medications', []),
            'key_metrics': [],
            'action_items': [],
            'progress_notes': []
        }

        # Extract condition and medication names for simpler memory format
        if isinstance(self.memory['conditions'], list) and len(self.memory['conditions']) > 0:
            if isinstance(self.memory['conditions'][0], dict):
                self.memory['conditions'] = [c.get('name', str(c)) for c in self.memory['conditions']]

        if isinstance(self.memory['medications'], list) and len(self.memory['medications']) > 0:
            if isinstance(self.memory['medications'][0], dict):
                self.memory['medications'] = [m.get('name', str(m)) for m in self.memory['medications']]

        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []

        # Build system prompt with all user data
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """
        Build the unified system prompt with all user data and memory.

        Returns:
            Rendered system prompt string
        """
        # Format user data for prompt (condensed version)
        user_data_summary = self._format_user_data()

        return render_prompt(
            UNIFIED_AGENT_PROMPT,
            user_data=user_data_summary,
            memory=self.memory
        )

    def _format_user_data(self) -> str:
        """
        Format user data into a readable summary for the prompt.

        Returns:
            Formatted user data string
        """
        sections = []

        # User profile
        if 'user_profile' in self.user_data:
            profile = self.user_data['user_profile']
            sections.append(f"""**User Profile:**
- Age: {profile.get('age')} years
- Gender: {profile.get('gender')}
- Height: {profile.get('height_cm')} cm
- Weight: {profile.get('weight_kg')} kg
- Activity Level: {profile.get('activity_level')}""")

        # Health records
        if 'health_context' in self.user_data:
            health_context = self.user_data['health_context']
            health_records = health_context.get('health_records', {})

            conditions = health_records.get('conditions', [])
            if conditions:
                cond_names = [c['name'] if isinstance(c, dict) else c for c in conditions]
                sections.append(f"**Medical Conditions:** {', '.join(cond_names)}")

            medications = health_records.get('medications', [])
            if medications:
                med_names = [f"{m['name']} ({m['dosage']})" if isinstance(m, dict) else m for m in medications]
                sections.append(f"**Medications:** {', '.join(med_names)}")

            allergies = health_records.get('allergies', [])
            if allergies:
                sections.append(f"**Allergies:** {', '.join(allergies)}")

            family_history = health_records.get('family_history', [])
            if family_history:
                sections.append(f"**Family History:** {', '.join(family_history)}")

        # Wearable data summary
        if 'personal_data' in self.user_data:
            personal_data = self.user_data['personal_data']
            metrics = personal_data.get('metrics_summary', {})
            if metrics:
                sections.append(f"""**Recent Health Metrics (30-day averages):**
- Resting Heart Rate: {metrics.get('avg_resting_heart_rate')} bpm
- Sleep Duration: {metrics.get('avg_sleep_hours')} hours
- Daily Steps: {metrics.get('avg_daily_steps')}
- Heart Rate Variability: {metrics.get('avg_hrv')} ms
- Sleep Quality Trend: {metrics.get('sleep_quality_trend')}
- Activity Consistency: {metrics.get('activity_consistency')}""")

            # Detailed time-series data availability
            wearable_data = personal_data.get('wearable_data', {})
            if wearable_data:
                data_points = []
                for key, value in wearable_data.items():
                    if isinstance(value, list):
                        data_points.append(f"{key} ({len(value)} measurements)")
                sections.append(f"**Available Time-Series Data:** {', '.join(data_points)}")

        # Lab results
        if 'lab_results' in self.user_data:
            lab_results = self.user_data['lab_results']
            sections.append(f"""**Recent Lab Results ({lab_results.get('last_test_date')}):**
- Total Cholesterol: {lab_results['results']['cholesterol_total']['value']} {lab_results['results']['cholesterol_total']['unit']}
- LDL: {lab_results['results']['ldl_cholesterol']['value']} {lab_results['results']['ldl_cholesterol']['unit']}
- HDL: {lab_results['results']['hdl_cholesterol']['value']} {lab_results['results']['hdl_cholesterol']['unit']}
- Fasting Glucose: {lab_results['results']['glucose_fasting']['value']} {lab_results['results']['glucose_fasting']['unit']}
- HbA1c: {lab_results['results']['hba1c']['value']}{lab_results['results']['hba1c']['unit']}
- Vitamin D: {lab_results['results']['vitamin_d']['value']} {lab_results['results']['vitamin_d']['unit']}""")

        return "\n\n".join(sections)

    def _format_conversation_history(self, max_turns: int = 5) -> str:
        """
        Format recent conversation history for context.

        Args:
            max_turns: Maximum number of conversation turns to include

        Returns:
            Formatted conversation history
        """
        if not self.conversation_history:
            return "No previous conversation"

        recent = self.conversation_history[-max_turns * 2:]  # Last N turns (user + assistant)
        formatted = []

        for turn in recent:
            role = turn['role'].capitalize()
            content = turn['content']
            formatted.append(f"{role}: {content}")

        return "\n\n".join(formatted)

    def _build_user_prompt(self, user_query: str) -> str:
        """
        Build the user prompt with query and conversation context.

        Args:
            user_query: The user's current query

        Returns:
            Formatted user prompt
        """
        conversation_context = self._format_conversation_history()

        if conversation_context == "No previous conversation":
            return f"""User Query: {user_query}

Please respond to this query by drawing on your data analysis, medical expertise, and coaching skills as appropriate."""
        else:
            return f"""Conversation History:
{conversation_context}

Current User Query: {user_query}

Please respond to this query by drawing on your data analysis, medical expertise, and coaching skills as appropriate. Maintain conversation context from the history above."""

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query with the unified agent.

        This is the main entry point - a single LLM call handles the entire query.

        Args:
            user_query: The user's health-related query

        Returns:
            Dictionary containing:
                - query: Original user query
                - response: Agent's response
                - updated_memory: Current memory state
                - conversation_length: Number of turns so far
        """
        # Single LLM call with full context
        user_prompt = self._build_user_prompt(user_query)

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.6  # Balanced temperature for conversational + analytical
        )

        # Update memory after response
        self.update_memory(user_query, response)

        # Update conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_query
        })
        self.conversation_history.append({
            'role': 'assistant',
            'content': response
        })

        # Rebuild system prompt with updated memory for next turn
        self.system_prompt = self._build_system_prompt()

        return {
            'query': user_query,
            'response': response,
            'updated_memory': self.memory,
            'conversation_length': len(self.conversation_history) // 2
        }

    def update_memory(self, user_query: str, agent_response: str):
        """
        Extract and update memory entities from conversation turn.

        Uses LLM to extract key entities (goals, conditions, actions, etc.)
        from the current conversation turn.

        Args:
            user_query: The user's query
            agent_response: The agent's response
        """
        user_prompt = render_prompt(
            UNIFIED_MEMORY_UPDATE_PROMPT,
            user_query=user_query,
            agent_response=agent_response,
            current_memory=json.dumps(self.memory, indent=2)
        )

        response = call_gemini(
            system_prompt="You are a helpful assistant that extracts structured information from conversations.",
            user_prompt=user_prompt,
            temperature=0.3  # Lower temperature for structured extraction
        )

        # Parse and merge with existing memory
        try:
            updated_memory = self._extract_json(response)

            # Merge lists (append only new items)
            for key in ['goals', 'conditions', 'medications', 'key_metrics', 'action_items', 'progress_notes']:
                if key in updated_memory and isinstance(updated_memory[key], list):
                    # Add new items that aren't already present
                    existing = set(str(item) for item in self.memory.get(key, []))
                    new_items = [item for item in updated_memory[key] if str(item) not in existing]
                    self.memory[key] = self.memory.get(key, []) + new_items

            # Merge lifestyle dictionary
            if 'lifestyle' in updated_memory and isinstance(updated_memory['lifestyle'], dict):
                self.memory['lifestyle'].update(updated_memory['lifestyle'])

        except (json.JSONDecodeError, ValueError):
            # If parsing fails, skip memory update for this turn
            pass

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from text that may contain markdown code blocks.

        Args:
            text: Text potentially containing JSON

        Returns:
            Parsed JSON dictionary
        """
        # Try to find JSON in code blocks first
        if '```json' in text:
            start = text.find('```json') + 7
            end = text.find('```', start)
            json_text = text[start:end].strip()
        elif '```' in text:
            start = text.find('```') + 3
            end = text.find('```', start)
            json_text = text[start:end].strip()
        else:
            # Try to find JSON object boundaries
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_text = text[start:end]
            else:
                json_text = text

        return json.loads(json_text)

    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current conversation state.

        Returns:
            Dictionary with conversation statistics and memory
        """
        return {
            'total_turns': len(self.conversation_history) // 2,
            'memory': self.memory,
            'recent_conversation': self.conversation_history[-6:] if self.conversation_history else []
        }
