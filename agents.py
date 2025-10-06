"""
Agent implementations for the Personal Health Agent (PHA) multi-agent system.

This module contains three specialized agents:
1. DataScienceAgent - Statistical analysis of time-series health data
2. DomainExpertAgent - Medical knowledge and health advice
3. HealthCoachAgent - Personalized coaching and behavior change support
"""

from api_client import call_gemini
from prompts import (
    get_agent_prompt,
    DS_CODE_GENERATION_PROMPT,
    HC_RECOMMENDATION_PROMPT,
    render_prompt
)
import json
from typing import Dict, Any, Optional, List


class DataScienceAgent:
    """
    Data Science Agent: Analyzes time-series wearable and health data.

    Implements a two-stage process:
    1. Generate statistical analysis plan
    2. Generate executable Python code to execute the plan
    """

    def __init__(self, personal_data: Dict[str, Any]):
        """
        Initialize the Data Science Agent.

        Args:
            personal_data: Dictionary containing user's wearable and health data
        """
        self.personal_data = personal_data
        self.system_prompt = get_agent_prompt('DS', personal_data=json.dumps(personal_data, indent=2))

    def generate_analysis_plan(self, user_query: str, data_summary: Optional[str] = None) -> str:
        """
        Generate a statistical analysis plan for the user's query.

        Args:
            user_query: The user's health-related question or request
            data_summary: Optional summary of available data

        Returns:
            Detailed analysis plan as a string
        """
        if data_summary is None:
            data_summary = self._summarize_available_data()

        user_prompt = f"""Analyze this user query and create a detailed analysis plan.

User Query: {user_query}

Create a Discussion section analyzing feasibility and operationalizing any vague terms, followed by an Approach section with numbered steps for the analysis."""

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.3  # Lower temperature for more structured planning
        )

        return response

    def generate_analysis_code(self, analysis_plan: str, user_query: str) -> str:
        """
        Generate executable Python code to implement the analysis plan.

        Args:
            analysis_plan: The previously generated analysis plan
            user_query: The original user query

        Returns:
            Python code as a string
        """
        data_variables = self._get_data_variables()

        user_prompt = render_prompt(
            DS_CODE_GENERATION_PROMPT,
            analysis_plan=analysis_plan,
            user_query=user_query,
            data_variables=data_variables
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.2  # Very low temperature for code generation
        )

        return response

    def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """
        Complete two-stage analysis: plan generation + code generation.

        Args:
            user_query: The user's health-related question

        Returns:
            Dictionary containing analysis plan and generated code
        """
        # Stage 1: Generate analysis plan
        analysis_plan = self.generate_analysis_plan(user_query)

        # Stage 2: Generate code
        analysis_code = self.generate_analysis_code(analysis_plan, user_query)

        return {
            'query': user_query,
            'analysis_plan': analysis_plan,
            'analysis_code': analysis_code,
            'status': 'code_generated'
        }

    def _summarize_available_data(self) -> str:
        """Generate a summary of available data for prompt context."""
        summary_parts = []

        if 'wearable_data' in self.personal_data:
            wearable = self.personal_data['wearable_data']
            summary_parts.append(f"Wearable Data: {', '.join(wearable.keys())}")

        if 'health_records' in self.personal_data:
            summary_parts.append("Health Records: Available")

        if 'time_range' in self.personal_data:
            summary_parts.append(f"Time Range: {self.personal_data['time_range']}")

        return "\n".join(summary_parts)

    def _get_data_variables(self) -> str:
        """Get a description of available data variables for code generation."""
        variables = []

        if 'wearable_data' in self.personal_data:
            for key, value in self.personal_data['wearable_data'].items():
                if isinstance(value, list):
                    variables.append(f"- {key}: list of {len(value)} data points")
                else:
                    variables.append(f"- {key}: {type(value).__name__}")

        return "\n".join(variables)


class DomainExpertAgent:
    """
    Domain Expert Agent: Medical knowledge base and health advisor.

    Integrates health records, wearable data, and medical knowledge to provide
    accurate, personalized health insights.
    """

    def __init__(self, user_health_context: Dict[str, Any]):
        """
        Initialize the Domain Expert Agent.

        Args:
            user_health_context: User's health profile, records, and context
        """
        self.user_health_context = user_health_context
        self.system_prompt = get_agent_prompt(
            'DE',
            user_health_context=json.dumps(user_health_context, indent=2)
        )

    def answer_health_question(
        self,
        user_question: str,
        wearable_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Answer a health-related question with medical accuracy.

        Args:
            user_question: The user's health question
            wearable_data: Optional recent wearable data for context

        Returns:
            Comprehensive answer as a string
        """
        health_profile = self._format_health_profile()
        wearable_summary = self._format_wearable_data(wearable_data) if wearable_data else "No recent data"

        user_prompt = f"""Answer this health question with medical accuracy and personalization.

User Question: {user_question}

User Health Profile:
{health_profile}

Recent Wearable Data:
{wearable_summary}

Provide a comprehensive answer that addresses the question, incorporates the user's personal context, and suggests actionable insights if appropriate."""

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.4
        )

        return response

    def synthesize_insights(
        self,
        user_query: str,
        ds_analysis: Optional[str] = None,
        lab_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Synthesize insights from multiple health data sources.

        Args:
            user_query: The user's query
            ds_analysis: Results from Data Science Agent analysis
            lab_results: Recent lab results if available

        Returns:
            Synthesized insights as a string
        """
        health_records = self.user_health_context.get('health_records', {})
        wearable_data = self.user_health_context.get('wearable_data', {})

        user_prompt = render_prompt(
            DE_SYNTHESIS_PROMPT,
            user_query=user_query,
            health_records=json.dumps(health_records, indent=2),
            wearable_data=json.dumps(wearable_data, indent=2),
            lab_results=json.dumps(lab_results, indent=2) if lab_results else "No recent lab results",
            ds_analysis=ds_analysis or "No statistical analysis available"
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.5
        )

        return response

    def _format_health_profile(self) -> str:
        """Format user's health profile for prompt inclusion."""
        profile = self.user_health_context.get('health_profile', {})
        return json.dumps(profile, indent=2)

    def _format_wearable_data(self, wearable_data: Dict[str, Any]) -> str:
        """Format wearable data summary for prompt inclusion."""
        return json.dumps(wearable_data, indent=2)


class HealthCoachAgent:
    """
    Health Coach Agent: Personalized coaching using motivational interviewing.

    Guides users toward health goals through multi-turn conversations,
    incorporating insights from DS and DE agents.
    """

    def __init__(self, user_context: Dict[str, Any]):
        """
        Initialize the Health Coach Agent.

        Args:
            user_context: User's profile, goals, and conversation history
        """
        self.user_context = user_context
        self.conversation_history: List[Dict[str, str]] = []
        self.identified_goals: List[str] = []
        self.system_prompt = get_agent_prompt(
            'HC',
            user_context=json.dumps(user_context, indent=2),
            available_insights=""
        )

    def identify_goals(
        self,
        user_message: str,
        health_insights: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Engage with user to identify health goals and motivations.

        Args:
            user_message: User's latest message
            health_insights: Available insights from other agents

        Returns:
            Coaching response to help identify goals
        """
        conversation_summary = self._format_conversation_history()
        insights_summary = json.dumps(health_insights, indent=2) if health_insights else "No insights available yet"

        user_prompt = f"""Engage with the user to identify their health goals and motivations.

Conversation History:
{conversation_summary}

User's Latest Message: {user_message}

Available Health Insights: {insights_summary}

Use open-ended questions to explore deeper motivations, reflect back what you're hearing, and identify specific, measurable goals."""

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.7  # Higher temperature for more natural conversation
        )

        # Update conversation history
        self._add_to_history("user", user_message)
        self._add_to_history("coach", response)

        return response

    def provide_recommendations(
        self,
        user_goals: List[str],
        ds_insights: Optional[str] = None,
        de_insights: Optional[str] = None,
        stage: str = "initial"
    ) -> str:
        """
        Provide personalized health recommendations.

        Args:
            user_goals: List of identified user goals
            ds_insights: Insights from Data Science Agent
            de_insights: Insights from Domain Expert Agent
            stage: Stage of coaching (initial, progress_check, adjustment)

        Returns:
            Personalized recommendations
        """
        user_prompt = render_prompt(
            HC_RECOMMENDATION_PROMPT,
            user_goals="\n".join(f"- {goal}" for goal in user_goals),
            user_context=json.dumps(self.user_context, indent=2),
            ds_insights=ds_insights or "No data analysis available",
            de_insights=de_insights or "No medical insights available",
            stage=stage
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.6
        )

        return response

    def handle_feedback(
        self,
        previous_recommendation: str,
        user_feedback: str
    ) -> str:
        """
        Process user feedback and adjust coaching approach.

        Args:
            previous_recommendation: The previous recommendation given
            user_feedback: User's feedback on the recommendation

        Returns:
            Adjusted coaching response
        """
        conversation_summary = self._format_conversation_history()

        user_prompt = render_prompt(
            HC_FEEDBACK_PROCESSING_PROMPT,
            previous_recommendation=previous_recommendation,
            user_feedback=user_feedback,
            conversation_history=conversation_summary
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.7
        )

        # Update conversation history
        self._add_to_history("user", user_feedback)
        self._add_to_history("coach", response)

        return response

    def _format_conversation_history(self) -> str:
        """Format conversation history for prompt inclusion."""
        if not self.conversation_history:
            return "No previous conversation"

        history_lines = []
        for turn in self.conversation_history[-10:]:  # Last 10 turns
            role = turn['role'].capitalize()
            message = turn['message']
            history_lines.append(f"{role}: {message}")

        return "\n\n".join(history_lines)

    def _add_to_history(self, role: str, message: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            'role': role,
            'message': message,
            'timestamp': None  # Could add actual timestamp if needed
        })


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_agents(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Factory function to create all three agents with user data.

    Args:
        user_data: Complete user data including health context, wearable data, etc.

    Returns:
        Dictionary containing initialized agents
    """
    ds_agent = DataScienceAgent(
        personal_data=user_data.get('personal_data', {})
    )

    de_agent = DomainExpertAgent(
        user_health_context=user_data.get('health_context', {})
    )

    hc_agent = HealthCoachAgent(
        user_context=user_data.get('user_profile', {})
    )

    return {
        'ds': ds_agent,
        'de': de_agent,
        'hc': hc_agent
    }
