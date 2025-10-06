"""
Main entry point for the Personal Health Agent (PHA) multi-agent system.

This script demonstrates the end-to-end functionality of the PHA system,
including initialization, query processing, and interactive conversation.
"""

import sys
from agents import DataScienceAgent, DomainExpertAgent, HealthCoachAgent
from orchestrator import Orchestrator
from mock_data import get_mock_user_data, get_sample_queries, print_data_summary
import json


def initialize_system(verbose=False):
    """
    Initialize the PHA multi-agent system with mock data.

    Args:
        verbose: If True, show detailed initialization steps

    Returns:
        Initialized Orchestrator instance and user data
    """
    if verbose:
        print("\nInitializing Personal Health Agent...")

    # Get mock user data
    user_data = get_mock_user_data()

    # Initialize agents
    ds_agent = DataScienceAgent(
        personal_data=user_data['personal_data']
    )

    de_agent = DomainExpertAgent(
        user_health_context=user_data['health_context']
    )

    hc_agent = HealthCoachAgent(
        user_context=user_data['user_profile']
    )

    orchestrator = Orchestrator(
        ds_agent=ds_agent,
        de_agent=de_agent,
        hc_agent=hc_agent,
        initial_context={
            'goals': [],
            'conditions': [c['name'] for c in user_data['health_context']['health_records']['conditions']],
            'medications': [m['name'] for m in user_data['health_context']['health_records']['medications']],
            'lifestyle': {},
            'key_metrics': [],
            'action_items': [],
            'progress_notes': []
        }
    )

    if verbose:
        print("✓ System initialized\n")

    return orchestrator, user_data


def run_flow_mode(orchestrator: Orchestrator, query: str):
    """
    Run a query in flow mode - shows detailed agent orchestration and attribution.

    Args:
        orchestrator: Initialized Orchestrator instance
        query: User query to process
    """
    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    # Process the query
    result = orchestrator.process_query(query)
    plan = result['orchestration_plan']

    # Show flow visualization
    print("\n┌─ ORCHESTRATION FLOW")
    print("│")
    print(f"│  Intent: {plan.get('user_intent', 'N/A')}")
    print(f"│  Main Agent: {plan.get('main_agent', 'N/A')}")
    print(f"│  Supporting: {', '.join(plan.get('supporting_agents', []))}")
    print("│")

    # Show agent activity
    print("├─ AGENT ACTIVITY")
    for agent_name, task in plan.get('tasks', {}).items():
        if task:
            status = "✓" if agent_name in result['agent_responses'] else "○"
            print(f"│  {status} {agent_name}: {task[:60]}...")
    print("│")

    # Show quality check
    reflection = result['reflection']
    approved = reflection.get('approved', True)
    print(f"├─ QUALITY CHECK: {'✓ Approved' if approved else '✗ Issues found'}")
    print("│")

    # Show final response with attribution
    print("└─ FINAL RESPONSE")
    print("\n" + "-" * 60)
    print(result['response'])
    print("-" * 60)

    # Attribution summary
    print(f"\n[Main: {plan.get('main_agent', 'N/A')} | " +
          f"Supporting: {', '.join(plan.get('supporting_agents', []))}]")

    return result


def run_interactive_mode(orchestrator: Orchestrator):
    """
    Run an interactive conversation loop with the PHA system.

    Args:
        orchestrator: Initialized Orchestrator instance
    """
    print("\n" + "─" * 60)
    print("Personal Health Agent - Interactive Mode")
    print("─" * 60)
    print("\nCommands: 'quit' to exit | 'memory' to view context | 'summary' for stats\n")

    while True:
        # Get user input
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Check for special commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using PHA. Stay healthy!\n")
            break

        if user_input.lower() == 'memory':
            print("\n" + json.dumps(orchestrator.memory, indent=2) + "\n")
            continue

        if user_input.lower() == 'summary':
            summary = orchestrator.get_conversation_summary()
            print(f"\nTurns: {summary['total_turns']} | " +
                  f"Goals: {len(orchestrator.memory['goals'])} | " +
                  f"Actions: {len(orchestrator.memory['action_items'])}\n")
            continue

        # Process the query
        try:
            result = orchestrator.process_query(user_input)
            print(f"\nPHA: {result['response']}\n")
        except Exception as e:
            print(f"\n✗ Error: {e}\n")
            print("Please try again or type 'quit' to exit.\n")


def run_data_mode():
    """Display mock data summary and exit."""
    print("\n" + "─" * 60)
    print("Personal Health Agent - Data Testing Mode")
    print("─" * 60 + "\n")
    print_data_summary()


def main():
    """Main entry point for the PHA system."""

    # Parse command line arguments
    mode = 'interactive'  # Default mode
    query = None

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        # For flow mode, allow passing a query
        if mode == 'flow' and len(sys.argv) > 2:
            query = ' '.join(sys.argv[2:])

    # Handle data mode separately (no initialization needed)
    if mode == 'data':
        run_data_mode()
        return

    # Initialize system (verbose only for flow mode)
    verbose = mode == 'flow'
    if verbose:
        print("\n✓ Initializing...")

    try:
        orchestrator, user_data = initialize_system(verbose=verbose)
        if verbose:
            print("✓ System ready")
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Activate virtual environment: source .venv/bin/activate")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Set API key: export GOOGLE_API_KEY='your-key-here'")
        return

    if mode == 'interactive' or mode == 'i':
        print(f"✓ Mode: Interactive")
        run_interactive_mode(orchestrator)

    elif mode == 'flow' or mode == 'f':
        print(f"✓ Mode: Flow Visualization\n")
        # Use provided query or default sample query
        if not query:
            sample_queries = get_sample_queries()
            query = sample_queries[0]
        run_flow_mode(orchestrator, query)

    else:
        print(f"\n✗ Unknown mode: {mode}")
        print("Valid modes: interactive (default), flow, data")
        sys.exit(1)


if __name__ == "__main__":
    # Show usage only if no arguments or invalid mode
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] not in ['interactive', 'i', 'flow', 'f', 'data']):
        print("\nPersonal Health Agent - Multi-Agent System")
        print("Based on arXiv 2508.20148\n")
        print("Usage: python main.py [mode] [options]")
        print("\nModes:")
        print("  interactive  - Conversational mode (default)")
        print("  flow         - Show agent orchestration flow")
        print("  data         - Display mock data summary")
        print("\nExamples:")
        print("  python main.py")
        print("  python main.py interactive")
        print("  python main.py flow \"How has my sleep been?\"")
        print("  python main.py data")
        print()

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
