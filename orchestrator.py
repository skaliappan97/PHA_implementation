"""
Orchestrator for the Personal Health Agent (PHA) multi-agent system.

The Orchestrator coordinates three specialized agents (DS, DE, HC) to provide
comprehensive health insights through a structured 4-step process.
"""

from api_client import call_gemini
from agents import DataScienceAgent, DomainExpertAgent, HealthCoachAgent
from prompts import (
    get_agent_prompt,
    ORCHESTRATOR_TASK_ASSIGNMENT_PROMPT,
    ORCHESTRATOR_REFLECTION_PROMPT,
    ORCHESTRATOR_MEMORY_UPDATE_PROMPT,
    render_prompt
)
import json
from typing import Dict, Any, List, Optional


class Orchestrator:
    """
    Central coordinator for the multi-agent Personal Health Agent system.

    Implements a 4-step process for each user query:
    1. User Need Understanding - Analyze query and determine required agents
    2. Agent Orchestration - Assign main/supporting agents and route tasks
    3. Query Reflection - Review synthesized information for quality
    4. Memory Update - Log key entities for conversation context
    """

    def __init__(
        self,
        ds_agent: DataScienceAgent,
        de_agent: DomainExpertAgent,
        hc_agent: HealthCoachAgent,
        initial_context: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Orchestrator with three specialized agents.

        Args:
            ds_agent: Data Science Agent instance
            de_agent: Domain Expert Agent instance
            hc_agent: Health Coach Agent instance
            initial_context: Optional initial context/memory
        """
        self.ds_agent = ds_agent
        self.de_agent = de_agent
        self.hc_agent = hc_agent

        # Conversation memory
        self.memory = initial_context or {
            'goals': [],
            'conditions': [],
            'lifestyle': {},
            'medications': [],
            'key_metrics': [],
            'action_items': [],
            'progress_notes': []
        }

        self.conversation_history: List[Dict[str, str]] = []

        # System prompt for orchestration decisions
        self.system_prompt = get_agent_prompt(
            'ORCHESTRATOR',
            context=json.dumps(self.memory, indent=2)
        )

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query through the complete 4-step orchestration process.

        Args:
            user_query: The user's health-related query

        Returns:
            Dictionary containing the final response and metadata
        """
        # Step 1: Understand user need
        orchestration_plan = self.understand_user_need(user_query)

        # Step 2: Orchestrate agents
        agent_responses = self.orchestrate_agents(user_query, orchestration_plan)

        # Synthesize response
        final_response = self._synthesize_response(
            user_query,
            orchestration_plan,
            agent_responses
        )

        # Step 3: Reflect on response
        reflection_result = self.reflect_on_response(
            user_query,
            orchestration_plan,
            agent_responses,
            final_response
        )

        # If reflection fails, improve response
        if not reflection_result.get('approved', True):
            final_response = self._improve_response(
                final_response,
                reflection_result.get('suggested_improvements', '')
            )

        # Step 4: Update memory
        self.update_memory(user_query, final_response)

        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_query
        })
        self.conversation_history.append({
            'role': 'assistant',
            'content': final_response
        })

        return {
            'query': user_query,
            'response': final_response,
            'orchestration_plan': orchestration_plan,
            'agent_responses': agent_responses,
            'reflection': reflection_result,
            'updated_memory': self.memory
        }

    def understand_user_need(self, user_query: str) -> Dict[str, Any]:
        """
        Step 1: Analyze user query to determine which agents are needed.

        Args:
            user_query: The user's query

        Returns:
            Orchestration plan with main/supporting agents and tasks
        """
        conversation_summary = self._format_conversation_history()
        user_context_summary = json.dumps(self.memory, indent=2)

        user_prompt = render_prompt(
            ORCHESTRATOR_TASK_ASSIGNMENT_PROMPT,
            user_query=user_query,
            conversation_history=conversation_summary
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )

        # Parse JSON response
        try:
            plan = self._extract_json(response)
        except json.JSONDecodeError:
            # Fallback: basic orchestration if JSON parsing fails
            plan = {
                'user_intent': 'General health query',
                'main_agent': 'HC',
                'supporting_agents': ['DE'],
                'tasks': {
                    'DE': 'Provide health information',
                    'HC': 'Synthesize and provide personalized guidance'
                }
            }

        return plan

    def orchestrate_agents(
        self,
        user_query: str,
        orchestration_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Step 2: Route tasks to appropriate agents and collect responses.

        Args:
            user_query: The user's query
            orchestration_plan: Plan from understand_user_need

        Returns:
            Dictionary of agent responses
        """
        agent_responses = {}
        tasks = orchestration_plan.get('tasks', {})

        # Execute DS agent tasks
        if 'DS' in tasks and tasks['DS']:
            try:
                ds_result = self.ds_agent.analyze_query(user_query)
                agent_responses['DS'] = ds_result
            except Exception as e:
                agent_responses['DS'] = {'error': str(e)}

        # Execute DE agent tasks
        if 'DE' in tasks and tasks['DE']:
            try:
                # Check if we have DS insights to include
                ds_insights = None
                if 'DS' in agent_responses:
                    ds_insights = agent_responses['DS'].get('analysis_plan', '')

                de_result = self.de_agent.synthesize_insights(
                    user_query=user_query,
                    ds_analysis=ds_insights
                )
                agent_responses['DE'] = de_result
            except Exception as e:
                agent_responses['DE'] = {'error': str(e)}

        # Execute HC agent tasks
        if 'HC' in tasks and tasks['HC']:
            try:
                # Gather insights from other agents
                health_insights = {
                    'ds': agent_responses.get('DS'),
                    'de': agent_responses.get('DE')
                }

                # Determine if this is goal identification or recommendation
                if 'goal' in tasks['HC'].lower() or 'motivation' in tasks['HC'].lower():
                    hc_result = self.hc_agent.identify_goals(
                        user_message=user_query,
                        health_insights=health_insights
                    )
                else:
                    # Extract goals from memory
                    user_goals = self.memory.get('goals', ['Improve overall health'])

                    hc_result = self.hc_agent.provide_recommendations(
                        user_goals=user_goals,
                        ds_insights=str(agent_responses.get('DS', '')),
                        de_insights=str(agent_responses.get('DE', ''))
                    )

                agent_responses['HC'] = hc_result
            except Exception as e:
                agent_responses['HC'] = {'error': str(e)}

        return agent_responses

    def reflect_on_response(
        self,
        user_query: str,
        orchestration_plan: Dict[str, Any],
        agent_responses: Dict[str, Any],
        proposed_response: str
    ) -> Dict[str, Any]:
        """
        Step 3: Review synthesized response for quality before presenting to user.

        Args:
            user_query: Original user query
            orchestration_plan: The orchestration plan used
            agent_responses: Responses from agents
            proposed_response: The synthesized response to review

        Returns:
            Dictionary with approval status and feedback
        """
        user_prompt = render_prompt(
            ORCHESTRATOR_REFLECTION_PROMPT,
            user_query=user_query,
            orchestration_plan=json.dumps(orchestration_plan, indent=2),
            agent_responses=json.dumps(agent_responses, indent=2),
            proposed_response=proposed_response
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.2
        )

        # Parse reflection result
        try:
            reflection = self._extract_json(response)
        except json.JSONDecodeError:
            # Default to approved if parsing fails
            reflection = {
                'approved': True,
                'issues': [],
                'suggested_improvements': ''
            }

        return reflection

    def update_memory(self, user_query: str, final_response: str):
        """
        Step 4: Extract and log key entities from conversation turn.

        Args:
            user_query: The user's query
            final_response: The final response given to user

        Updates:
            self.memory with extracted entities
        """
        user_prompt = render_prompt(
            ORCHESTRATOR_MEMORY_UPDATE_PROMPT,
            user_query=user_query,
            final_response=final_response,
            current_memory=json.dumps(self.memory, indent=2)
        )

        response = call_gemini(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )

        # Parse and update memory
        try:
            updated_memory = self._extract_json(response)
            # Merge with existing memory (don't overwrite, append)
            for key in ['goals', 'conditions', 'medications', 'key_metrics', 'action_items', 'progress_notes']:
                if key in updated_memory:
                    if isinstance(updated_memory[key], list):
                        # Add new items that aren't already present
                        existing = set(str(item) for item in self.memory.get(key, []))
                        new_items = [item for item in updated_memory[key] if str(item) not in existing]
                        self.memory[key] = self.memory.get(key, []) + new_items

            # For lifestyle (dict), merge
            if 'lifestyle' in updated_memory:
                self.memory['lifestyle'].update(updated_memory['lifestyle'])

        except json.JSONDecodeError:
            # If parsing fails, skip memory update for this turn
            pass

    def _synthesize_response(
        self,
        user_query: str,
        orchestration_plan: Dict[str, Any],
        agent_responses: Dict[str, Any]
    ) -> str:
        """
        Synthesize agent responses into a coherent user-facing response.

        Args:
            user_query: Original query
            orchestration_plan: Orchestration plan
            agent_responses: Responses from all agents

        Returns:
            Synthesized response string
        """
        main_agent = orchestration_plan.get('main_agent', 'HC')

        # The main agent's response forms the core
        main_response = agent_responses.get(main_agent, '')

        # If main response is a dict (like DS agent), extract relevant text
        if isinstance(main_response, dict):
            if 'error' in main_response:
                main_response = f"I encountered an issue: {main_response['error']}"
            elif main_agent == 'DS':
                main_response = f"Based on my analysis:\n\n{main_response.get('analysis_plan', '')}"

        # For Health Coach as main agent, we typically return their response directly
        # as they synthesize other agents' inputs
        if main_agent == 'HC':
            return str(main_response)

        # For DS or DE as main agent, add HC perspective if available
        if 'HC' in agent_responses and main_agent != 'HC':
            hc_response = agent_responses['HC']
            if hc_response and not isinstance(hc_response, dict):
                return f"{main_response}\n\n{hc_response}"

        return str(main_response)

    def _improve_response(
        self,
        original_response: str,
        improvements: str
    ) -> str:
        """
        Improve response based on reflection feedback.

        Args:
            original_response: The original response
            improvements: Suggested improvements

        Returns:
            Improved response
        """
        prompt = f"""The following response needs improvement:

Original Response:
{original_response}

Suggested Improvements:
{improvements}

Please provide an improved version that addresses these concerns while maintaining
the helpful and personalized nature of the response."""

        improved = call_gemini(
            system_prompt="You are a health communication expert improving responses for clarity and completeness.",
            user_prompt=prompt,
            temperature=0.5
        )

        return improved

    def _format_conversation_history(self, max_turns: int = 5) -> str:
        """Format recent conversation history for prompts."""
        if not self.conversation_history:
            return "No previous conversation"

        recent = self.conversation_history[-max_turns * 2:]  # Last N turns (user + assistant pairs)
        formatted = []

        for turn in recent:
            role = turn['role'].capitalize()
            content = turn['content']
            formatted.append(f"{role}: {content}")

        return "\n\n".join(formatted)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from text that may contain markdown code blocks or other text.

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
            Dictionary with conversation stats and memory
        """
        return {
            'total_turns': len(self.conversation_history) // 2,
            'memory': self.memory,
            'recent_conversation': self.conversation_history[-6:] if self.conversation_history else []
        }
