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


def initialize_system():
    """
    Initialize the PHA multi-agent system with mock data.

    Returns:
        Initialized Orchestrator instance
    """
    print("\n" + "=" * 80)
    print("PERSONAL HEALTH AGENT (PHA) - Multi-Agent System")
    print("=" * 80)
    print("\nInitializing system...")

    # Get mock user data
    user_data = get_mock_user_data()

    # Initialize agents
    print("\n Creating Data Science Agent...")
    ds_agent = DataScienceAgent(
        personal_data=user_data['personal_data']
    )

    print(" Creating Domain Expert Agent...")
    de_agent = DomainExpertAgent(
        user_health_context=user_data['health_context']
    )

    print(" Creating Health Coach Agent...")
    hc_agent = HealthCoachAgent(
        user_context=user_data['user_profile']
    )

    print(" Creating Orchestrator...")
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

    print("\n System initialized successfully!\n")

    return orchestrator, user_data


def run_single_query_demo(orchestrator: Orchestrator, query: str):
    """
    Run a single query through the system and display results.

    Args:
        orchestrator: Initialized Orchestrator instance
        query: User query to process
    """
    print("\n" + "=" * 80)
    print(f"USER QUERY: {query}")
    print("=" * 80)

    print("\n= Processing query through multi-agent system...")

    # Process the query
    result = orchestrator.process_query(query)

    # Display orchestration plan
    print("\n= ORCHESTRATION PLAN")
    print("-" * 80)
    plan = result['orchestration_plan']
    print(f"Intent: {plan.get('user_intent', 'N/A')}")
    print(f"Main Agent: {plan.get('main_agent', 'N/A')}")
    print(f"Supporting Agents: {', '.join(plan.get('supporting_agents', []))}")

    # Display agent responses summary
    print("\n> AGENT RESPONSES")
    print("-" * 80)
    for agent_name, response in result['agent_responses'].items():
        print(f"\n{agent_name} Agent:")
        if isinstance(response, dict):
            if 'error' in response:
                print(f"  L Error: {response['error']}")
            else:
                print(f"   Response generated ({len(str(response))} chars)")
        else:
            print(f"   Response: {response[:150]}..." if len(response) > 150 else f"   {response}")

    # Display reflection result
    print("\n= QUALITY REFLECTION")
    print("-" * 80)
    reflection = result['reflection']
    approved = reflection.get('approved', True)
    print(f"Approved: {' Yes' if approved else 'L No'}")
    if not approved:
        print(f"Issues: {reflection.get('issues', [])}")

    # Display final response
    print("\n= FINAL RESPONSE TO USER")
    print("=" * 80)
    print(result['response'])
    print("=" * 80)

    # Display updated memory
    print("\n> UPDATED MEMORY")
    print("-" * 80)
    memory = result['updated_memory']
    print(f"Goals: {len(memory.get('goals', []))} items")
    print(f"Conditions: {len(memory.get('conditions', []))} items")
    print(f"Action Items: {len(memory.get('action_items', []))} items")

    return result


def run_interactive_mode(orchestrator: Orchestrator):
    """
    Run an interactive conversation loop with the PHA system.

    Args:
        orchestrator: Initialized Orchestrator instance
    """
    print("\n" + "=" * 80)
    print("=  INTERACTIVE MODE")
    print("=" * 80)
    print("\nYou can now have a conversation with your Personal Health Agent.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Type 'memory' to see the current conversation memory.")
    print("Type 'summary' to see a conversation summary.")
    print("\n" + "-" * 80 + "\n")

    while True:
        # Get user input
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Check for special commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n=K Thank you for using the Personal Health Agent. Stay healthy!")
            break

        if user_input.lower() == 'memory':
            print("\n> Current Memory:")
            print(json.dumps(orchestrator.memory, indent=2))
            print()
            continue

        if user_input.lower() == 'summary':
            summary = orchestrator.get_conversation_summary()
            print(f"\n= Conversation Summary:")
            print(f"Total turns: {summary['total_turns']}")
            print(f"Goals tracked: {len(orchestrator.memory['goals'])}")
            print(f"Action items: {len(orchestrator.memory['action_items'])}")
            print()
            continue

        # Process the query
        print("\n= Processing...\n")
        try:
            result = orchestrator.process_query(user_input)
            print(f"PHA: {result['response']}\n")
        except Exception as e:
            print(f"\nL Error processing query: {e}\n")
            print("Please try again or type 'quit' to exit.\n")


def run_batch_demo(orchestrator: Orchestrator, sample_queries: list, num_queries: int = 3):
    """
    Run multiple sample queries in batch mode.

    Args:
        orchestrator: Initialized Orchestrator instance
        sample_queries: List of sample queries
        num_queries: Number of queries to run
    """
    print("\n" + "=" * 80)
    print("< BATCH DEMO MODE")
    print("=" * 80)
    print(f"\nRunning {num_queries} sample queries...\n")

    for i, query in enumerate(sample_queries[:num_queries], 1):
        print(f"\n{'=' * 80}")
        print(f"QUERY {i}/{num_queries}")
        print(f"{'=' * 80}")

        run_single_query_demo(orchestrator, query)

        if i < num_queries:
            input("\n  Press Enter to continue to next query...")


def main():
    """Main entry point for the PHA system."""

    # Parse command line arguments
    mode = 'demo'  # Default mode
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    # Initialize the system
    orchestrator, user_data = initialize_system()

    # Show data summary
    if mode in ['demo', 'data']:
        print_data_summary()

    if mode == 'data':
        # Just show data and exit
        return

    # Get sample queries
    sample_queries = get_sample_queries()

    if mode == 'interactive' or mode == 'i':
        # Run interactive mode
        run_interactive_mode(orchestrator)

    elif mode == 'batch':
        # Run batch demo with all sample queries
        run_batch_demo(orchestrator, sample_queries, num_queries=len(sample_queries))

    elif mode == 'single':
        # Run a single query
        if len(sys.argv) > 2:
            query = ' '.join(sys.argv[2:])
        else:
            query = sample_queries[0]
        run_single_query_demo(orchestrator, query)

    else:  # demo mode (default)
        # Run a demo with a few sample queries
        run_batch_demo(orchestrator, sample_queries, num_queries=2)

        # Offer to continue in interactive mode
        print("\n" + "=" * 80)
        choice = input("\nWould you like to continue in interactive mode? (y/n): ").strip().lower()
        if choice == 'y':
            run_interactive_mode(orchestrator)


if __name__ == "__main__":
    print("\n")
    print("TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW")
    print("Q           PERSONAL HEALTH AGENT - Multi-Agent System Demo                  Q")
    print("Q                                                                             Q")
    print("Q  Based on: 'The Anatomy of a Personal Health Agent' (arXiv 2508.20148)    Q")
    print("ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]")

    print("\nUsage:")
    print("  python main.py [mode]")
    print("\nModes:")
    print("  demo        - Run 2 sample queries and optionally continue interactively (default)")
    print("  interactive - Start interactive conversation mode")
    print("  batch       - Run all sample queries in sequence")
    print("  single      - Run a single query (provide query as additional arguments)")
    print("  data        - Show mock data summary and exit")
    print("\nExamples:")
    print("  python main.py")
    print("  python main.py interactive")
    print("  python main.py single How has my sleep been?")
    print()

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n=K Interrupted. Goodbye!")
    except Exception as e:
        print(f"\nL Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
