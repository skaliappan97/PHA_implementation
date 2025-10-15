"""
Simple test to verify UnifiedAgent structure without API calls.
"""

from unified_agent import UnifiedAgent
from mock_data import get_mock_user_data
import json

def test_unified_agent_initialization():
    """Test that UnifiedAgent initializes correctly."""
    print("Testing UnifiedAgent initialization...")

    user_data = get_mock_user_data()
    agent = UnifiedAgent(user_data)

    # Check memory structure
    assert 'goals' in agent.memory
    assert 'conditions' in agent.memory
    assert 'medications' in agent.memory
    assert 'lifestyle' in agent.memory
    assert 'key_metrics' in agent.memory
    assert 'action_items' in agent.memory
    assert 'progress_notes' in agent.memory

    print("✓ Memory structure initialized correctly")
    print(f"  - Conditions: {agent.memory['conditions']}")
    print(f"  - Medications: {agent.memory['medications']}")

    # Check conversation history
    assert isinstance(agent.conversation_history, list)
    assert len(agent.conversation_history) == 0
    print("✓ Conversation history initialized correctly")

    # Check system prompt was built
    assert agent.system_prompt is not None
    assert len(agent.system_prompt) > 0
    print("✓ System prompt built successfully")
    print(f"  - Prompt length: {len(agent.system_prompt)} characters")

    # Check user data formatting
    user_data_summary = agent._format_user_data()
    assert 'User Profile' in user_data_summary
    assert 'Recent Health Metrics' in user_data_summary
    print("✓ User data formatted correctly")

    print("\n✅ All initialization tests passed!\n")

    return agent

def test_conversation_flow():
    """Test conversation history management."""
    print("Testing conversation flow...")

    user_data = get_mock_user_data()
    agent = UnifiedAgent(user_data)

    # Simulate adding to conversation history
    agent.conversation_history.append({
        'role': 'user',
        'content': 'How has my sleep been?'
    })
    agent.conversation_history.append({
        'role': 'assistant',
        'content': 'Your sleep has averaged 7.2 hours per night.'
    })

    # Test conversation formatting
    formatted = agent._format_conversation_history()
    assert 'User: How has my sleep been?' in formatted
    assert 'Assistant: Your sleep has averaged' in formatted
    print("✓ Conversation history formatting works")

    # Test summary
    summary = agent.get_conversation_summary()
    assert summary['total_turns'] == 1
    assert len(summary['recent_conversation']) == 2
    print("✓ Conversation summary works")
    print(f"  - Total turns: {summary['total_turns']}")

    print("\n✅ All conversation flow tests passed!\n")

def test_memory_structure():
    """Test memory extraction structure."""
    print("Testing memory structure...")

    user_data = get_mock_user_data()
    agent = UnifiedAgent(user_data)

    # Simulate memory update
    test_json = {
        'goals': ['Improve sleep quality'],
        'conditions': [],
        'lifestyle': {'exercise_frequency': '3x per week'},
        'medications': [],
        'key_metrics': ['sleep_hours'],
        'action_items': ['Track sleep for 2 weeks'],
        'progress_notes': []
    }

    # Test JSON extraction
    json_text = json.dumps(test_json)
    extracted = agent._extract_json(json_text)
    assert extracted['goals'] == ['Improve sleep quality']
    assert extracted['lifestyle']['exercise_frequency'] == '3x per week'
    print("✓ JSON extraction works")

    # Test JSON extraction from code blocks
    code_block = f"Here's the data:\n```json\n{json_text}\n```"
    extracted = agent._extract_json(code_block)
    assert extracted['goals'] == ['Improve sleep quality']
    print("✓ JSON extraction from code blocks works")

    print("\n✅ All memory structure tests passed!\n")

if __name__ == "__main__":
    print("=" * 60)
    print("UNIFIED AGENT STRUCTURE TESTS")
    print("=" * 60 + "\n")

    try:
        agent = test_unified_agent_initialization()
        test_conversation_flow()
        test_memory_structure()

        print("=" * 60)
        print("ALL TESTS PASSED ✅")
        print("=" * 60)
        print("\nUnifiedAgent is ready for use!")
        print("\nTo test with actual queries (requires API key):")
        print("  python main.py single")
        print("  python main.py compare \"Your query here\"")
        print("  python comparison.py --query \"Your query here\"")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
