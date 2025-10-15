"""
Comparison framework for evaluating multi-agent vs single-agent architectures.

This module provides tools to compare the performance, quality, and efficiency
of the multi-agent orchestration system against the single unified agent baseline.
"""

import time
import json
from typing import Dict, Any, List
from agents import DataScienceAgent, DomainExpertAgent, HealthCoachAgent
from orchestrator import Orchestrator
from unified_agent import UnifiedAgent
from mock_data import get_mock_user_data, get_sample_queries


class AgentComparison:
    """
    Framework for comparing multi-agent vs single-agent performance.

    Tracks metrics like response time, LLM calls, and allows for
    qualitative comparison of response quality.
    """

    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize comparison framework with user data.

        Args:
            user_data: Complete user data for both systems
        """
        self.user_data = user_data
        self.results = {
            'multi_agent': [],
            'single_agent': []
        }

    def run_single_query_comparison(self, query: str, show_metrics: bool = False) -> Dict[str, Any]:
        """
        Run a single query through both systems and compare responses side-by-side.

        Args:
            query: User query to test
            show_metrics: If True, show timing and API call metrics (default: False)

        Returns:
            Dictionary with comparison results
        """
        # Initialize fresh instances
        multi_orchestrator = self._init_multi_agent()
        single_agent = UnifiedAgent(self.user_data)

        # Run multi-agent
        start_time = time.time()
        try:
            multi_result = multi_orchestrator.process_query(query)
            multi_time = time.time() - start_time
            multi_response = multi_result['response']
            multi_plan = multi_result['orchestration_plan']
            multi_success = True
        except Exception as e:
            multi_time = time.time() - start_time
            multi_response = f"Error: {e}"
            multi_plan = {}
            multi_success = False

        # Run single-agent
        start_time = time.time()
        try:
            single_result = single_agent.process_query(query)
            single_time = time.time() - start_time
            single_response = single_result['response']
            single_success = True
        except Exception as e:
            single_time = time.time() - start_time
            single_response = f"Error: {e}"
            single_success = False

        # Display side-by-side comparison
        self._display_side_by_side_comparison(
            query=query,
            multi_response=multi_response,
            single_response=single_response,
            multi_plan=multi_plan,
            multi_time=multi_time,
            single_time=single_time,
            show_metrics=show_metrics
        )

        # Store results
        comparison_result = {
            'query': query,
            'multi_agent': {
                'response': multi_response,
                'time': multi_time,
                'plan': multi_plan,
                'success': multi_success
            },
            'single_agent': {
                'response': single_response,
                'time': single_time,
                'success': single_success
            },
            'metrics': {
                'time_ratio': multi_time / single_time if single_time > 0 else 0,
                'multi_faster': multi_time < single_time if single_time > 0 else False
            }
        }

        self.results['multi_agent'].append(comparison_result['multi_agent'])
        self.results['single_agent'].append(comparison_result['single_agent'])

        return comparison_result

    def _display_side_by_side_comparison(
        self,
        query: str,
        multi_response: str,
        single_response: str,
        multi_plan: Dict[str, Any],
        multi_time: float,
        single_time: float,
        show_metrics: bool
    ):
        """
        Display responses side-by-side for easy quality comparison.

        Args:
            query: User query
            multi_response: Multi-agent response
            single_response: Single-agent response
            multi_plan: Multi-agent orchestration plan
            multi_time: Multi-agent response time
            single_time: Single-agent response time
            show_metrics: Whether to show timing metrics
        """
        import textwrap

        # Terminal width
        width = 160  # Wider for better side-by-side view
        col_width = (width - 3) // 2  # 3 for separator

        print(f"\n{'=' * width}")
        print("RESPONSE QUALITY COMPARISON")
        print(f"{'=' * width}\n")

        # Query
        print(f"Query: {query}\n")

        # Header
        header_left = "MULTI-AGENT SYSTEM".center(col_width)
        header_right = "SINGLE-AGENT SYSTEM".center(col_width)
        print(f"{header_left} │ {header_right}")
        print(f"{'─' * col_width}─┼─{'─' * col_width}")

        # Agent info (compact)
        if show_metrics:
            agents_left = f"Main: {multi_plan.get('main_agent', 'N/A')}, Supporting: {', '.join(multi_plan.get('supporting_agents', []))}"[:col_width]
            agents_right = "Unified (DS + DE + HC)"
            print(f"{agents_left:<{col_width}} │ {agents_right:<{col_width}}")
            print(f"{'─' * col_width}─┼─{'─' * col_width}")

        # Wrap responses for side-by-side display
        multi_lines = textwrap.wrap(multi_response, width=col_width - 2)
        single_lines = textwrap.wrap(single_response, width=col_width - 2)

        # Pad to same length
        max_lines = max(len(multi_lines), len(single_lines))
        multi_lines += [''] * (max_lines - len(multi_lines))
        single_lines += [''] * (max_lines - len(single_lines))

        # Print responses side-by-side
        for left, right in zip(multi_lines, single_lines):
            print(f"{left:<{col_width}} │ {right:<{col_width}}")

        print(f"{'─' * col_width}─┴─{'─' * col_width}")

        # Optional metrics footer
        if show_metrics:
            print(f"\n⏱  Response Time: Multi={multi_time:.2f}s | Single={single_time:.2f}s")
            print(f"📞 LLM Calls: Multi=5-7 | Single=2")

        print(f"\n{'=' * width}\n")

        # Evaluation prompt
        print("Compare the responses above based on:")
        print("  • Depth and thoroughness of analysis")
        print("  • Medical accuracy and clinical reasoning")
        print("  • Actionability and practical recommendations")
        print("  • Personalization to user's specific context")
        print("  • Clarity and helpfulness of explanation")
        print(f"\n{'=' * width}\n")

    def run_batch_comparison(self, queries: List[str], save_results: bool = True, show_metrics: bool = False) -> Dict[str, Any]:
        """
        Run multiple queries through both systems and generate report.

        Args:
            queries: List of queries to test
            save_results: Whether to save results to JSON file
            show_metrics: Whether to show timing and API metrics for each query

        Returns:
            Dictionary with aggregate metrics and results
        """
        print(f"\n{'=' * 160}")
        print(f"BATCH QUALITY COMPARISON: {len(queries)} queries")
        print(f"{'=' * 160}\n")
        print("Focus: Response quality evaluation across multiple query types\n")

        all_comparisons = []

        for i, query in enumerate(queries, 1):
            print(f"\n{'─' * 160}")
            print(f"QUERY {i}/{len(queries)}")
            print(f"{'─' * 160}\n")
            comparison = self.run_single_query_comparison(query, show_metrics=show_metrics)
            all_comparisons.append(comparison)

            # Prompt for evaluation after each query
            if i < len(queries):
                input("\nPress Enter to continue to next query...")

        # Calculate aggregate metrics
        multi_times = [c['multi_agent']['time'] for c in all_comparisons if c['multi_agent']['success']]
        single_times = [c['single_agent']['time'] for c in all_comparisons if c['single_agent']['success']]

        report = {
            'total_queries': len(queries),
            'avg_response_time': {
                'multi_agent': sum(multi_times) / len(multi_times) if multi_times else 0,
                'single_agent': sum(single_times) / len(single_times) if single_times else 0
            },
            'success_rate': {
                'multi_agent': sum(1 for c in all_comparisons if c['multi_agent']['success']) / len(queries),
                'single_agent': sum(1 for c in all_comparisons if c['single_agent']['success']) / len(queries)
            },
            'estimated_llm_calls': {
                'multi_agent': len(queries) * 6,  # Average 6 calls per query
                'single_agent': len(queries) * 2  # 2 calls per query (process + memory)
            },
            'comparisons': all_comparisons
        }

        # Print summary (only if metrics requested)
        if show_metrics:
            print(f"\n{'=' * 160}")
            print("BATCH COMPARISON SUMMARY")
            print(f"{'=' * 160}\n")

            print(f"📊 Total Queries: {report['total_queries']}\n")

            print(f"⏱  Average Response Time:")
            print(f"   Multi-Agent:  {report['avg_response_time']['multi_agent']:.2f}s")
            print(f"   Single-Agent: {report['avg_response_time']['single_agent']:.2f}s\n")

            print(f"🎯 Success Rate:")
            print(f"   Multi-Agent:  {report['success_rate']['multi_agent']*100:.1f}%")
            print(f"   Single-Agent: {report['success_rate']['single_agent']*100:.1f}%\n")

            print(f"📞 Estimated Total LLM Calls:")
            print(f"   Multi-Agent:  ~{report['estimated_llm_calls']['multi_agent']} calls")
            print(f"   Single-Agent: ~{report['estimated_llm_calls']['single_agent']} calls")
            print(f"   Reduction:    {((report['estimated_llm_calls']['multi_agent'] - report['estimated_llm_calls']['single_agent']) / report['estimated_llm_calls']['multi_agent'] * 100):.1f}% fewer calls with single-agent\n")

        if save_results:
            filename = f"comparison_results_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"💾 Full results saved to: {filename}\n")

        return report

    def _init_multi_agent(self) -> Orchestrator:
        """
        Initialize a fresh multi-agent orchestrator.

        Returns:
            Initialized Orchestrator instance
        """
        ds_agent = DataScienceAgent(
            personal_data=self.user_data['personal_data']
        )

        de_agent = DomainExpertAgent(
            user_health_context=self.user_data['health_context']
        )

        hc_agent = HealthCoachAgent(
            user_context=self.user_data['user_profile']
        )

        orchestrator = Orchestrator(
            ds_agent=ds_agent,
            de_agent=de_agent,
            hc_agent=hc_agent,
            initial_context={
                'goals': [],
                'conditions': [c['name'] for c in self.user_data['health_context']['health_records']['conditions']],
                'medications': [m['name'] for m in self.user_data['health_context']['health_records']['medications']],
                'lifestyle': {},
                'key_metrics': [],
                'action_items': [],
                'progress_notes': []
            }
        )

        return orchestrator


def main():
    """
    Main entry point for comparison testing.

    Usage:
        python comparison.py                         # Run comparison on first sample query
        python comparison.py --batch                 # Run on all sample queries
        python comparison.py --query "..."           # Run on custom query
        python comparison.py --batch --metrics       # Run batch with timing metrics
    """
    import sys

    user_data = get_mock_user_data()
    comparison = AgentComparison(user_data)

    # Check for metrics flag
    show_metrics = '--metrics' in sys.argv
    if show_metrics:
        sys.argv.remove('--metrics')

    if len(sys.argv) > 1:
        if sys.argv[1] == '--batch':
            # Run all sample queries
            queries = get_sample_queries()
            comparison.run_batch_comparison(queries, show_metrics=show_metrics)
        elif sys.argv[1] == '--query' and len(sys.argv) > 2:
            # Run custom query
            query = ' '.join(sys.argv[2:])
            comparison.run_single_query_comparison(query, show_metrics=show_metrics)
        else:
            print("Usage:")
            print("  python comparison.py                      # Run comparison on first sample query")
            print("  python comparison.py --batch              # Run on all sample queries (quality focus)")
            print("  python comparison.py --query '...'        # Run on custom query")
            print("  python comparison.py --batch --metrics    # Show timing metrics")
            print("\nBy default, focuses on response quality comparison without timing metrics.")
    else:
        # Default: run first sample query
        queries = get_sample_queries()
        comparison.run_single_query_comparison(queries[0], show_metrics=show_metrics)


if __name__ == "__main__":
    main()
