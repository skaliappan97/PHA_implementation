"""
Mock health data for testing the Personal Health Agent system.

This module provides realistic simulated data for:
- Wearable device data (heart rate, sleep, steps, etc.)
- Health records (conditions, medications, allergies)
- Lab results
- User profile information

Since we don't have access to the WEAR-ME dataset from the paper,
this provides a realistic substitute for development and testing.
"""

from datetime import datetime, timedelta
import random
from typing import Dict, Any, List


def generate_time_series(
    days: int = 30,
    base_value: float = 70,
    variance: float = 10,
    daily_pattern: bool = True
) -> List[Dict[str, Any]]:
    """
    Generate mock time-series data for wearable metrics.

    Args:
        days: Number of days of data
        base_value: Average value
        variance: Standard deviation
        daily_pattern: Whether to add daily cyclical patterns

    Returns:
        List of timestamped data points
    """
    data = []
    start_date = datetime.now() - timedelta(days=days)

    for day in range(days):
        # Generate 24 hourly data points per day
        for hour in range(24):
            timestamp = start_date + timedelta(days=day, hours=hour)

            # Add daily pattern (e.g., higher HR during day, lower at night)
            if daily_pattern:
                # Sine wave for daily cycle
                daily_factor = 1 + 0.3 * ((hour - 12) / 12)
            else:
                daily_factor = 1

            value = base_value * daily_factor + random.gauss(0, variance)

            data.append({
                'timestamp': timestamp.isoformat(),
                'value': round(value, 2)
            })

    return data


def generate_sleep_data(days: int = 30) -> List[Dict[str, Any]]:
    """Generate mock sleep data."""
    sleep_data = []
    start_date = datetime.now() - timedelta(days=days)

    for day in range(days):
        # Randomize sleep duration around 7-8 hours
        sleep_duration = random.gauss(7.5, 1.0)
        deep_sleep = sleep_duration * random.uniform(0.15, 0.25)
        rem_sleep = sleep_duration * random.uniform(0.20, 0.25)
        light_sleep = sleep_duration - deep_sleep - rem_sleep

        sleep_data.append({
            'date': (start_date + timedelta(days=day)).date().isoformat(),
            'total_sleep_hours': round(sleep_duration, 2),
            'deep_sleep_hours': round(deep_sleep, 2),
            'rem_sleep_hours': round(rem_sleep, 2),
            'light_sleep_hours': round(light_sleep, 2),
            'sleep_quality_score': round(random.uniform(60, 95), 1),
            'times_awakened': random.randint(0, 5)
        })

    return sleep_data


def generate_activity_data(days: int = 30) -> List[Dict[str, Any]]:
    """Generate mock daily activity data."""
    activity_data = []
    start_date = datetime.now() - timedelta(days=days)

    for day in range(days):
        # Weekday vs weekend pattern
        date = start_date + timedelta(days=day)
        is_weekend = date.weekday() >= 5

        base_steps = 8000 if is_weekend else 10000
        steps = int(random.gauss(base_steps, 2000))

        activity_data.append({
            'date': date.date().isoformat(),
            'steps': max(steps, 2000),  # Minimum 2000 steps
            'active_minutes': random.randint(20, 90),
            'calories_burned': random.randint(1800, 2800),
            'distance_km': round(steps * 0.0008, 2),  # Rough conversion
            'floors_climbed': random.randint(5, 25)
        })

    return activity_data


# ============================================================================
# COMPLETE MOCK USER DATA
# ============================================================================

MOCK_USER_DATA = {
    # Personal profile
    'user_profile': {
        'user_id': 'user_001',
        'age': 35,
        'gender': 'male',
        'height_cm': 178,
        'weight_kg': 82,
        'timezone': 'America/Los_Angeles',
        'activity_level': 'moderately_active'
    },

    # Health context
    'health_context': {
        'health_profile': {
            'age': 35,
            'gender': 'male',
            'height_cm': 178,
            'weight_kg': 82,
            'bmi': 25.9
        },
        'health_records': {
            'conditions': [
                {
                    'name': 'Pre-hypertension',
                    'diagnosed_date': '2023-03-15',
                    'status': 'monitoring'
                }
            ],
            'medications': [
                {
                    'name': 'Vitamin D3',
                    'dosage': '2000 IU',
                    'frequency': 'daily',
                    'started_date': '2023-01-10'
                }
            ],
            'allergies': ['penicillin'],
            'family_history': [
                'Type 2 Diabetes (father)',
                'Hypertension (mother)'
            ]
        },
        'wearable_data': {
            'heart_rate_resting_avg': 72,
            'sleep_avg_hours': 7.2,
            'steps_avg_daily': 9500,
            'last_sync': datetime.now().isoformat()
        }
    },

    # Detailed wearable data for DS agent
    'personal_data': {
        'time_range': '30 days',
        'wearable_data': {
            'heart_rate': generate_time_series(
                days=30,
                base_value=72,
                variance=8,
                daily_pattern=True
            ),
            'sleep': generate_sleep_data(days=30),
            'activity': generate_activity_data(days=30),
            'heart_rate_variability': generate_time_series(
                days=30,
                base_value=45,
                variance=8,
                daily_pattern=False
            )
        },
        'metrics_summary': {
            'avg_resting_heart_rate': 72,
            'avg_sleep_hours': 7.2,
            'avg_daily_steps': 9500,
            'avg_hrv': 45,
            'sleep_quality_trend': 'stable',
            'activity_consistency': 'moderate'
        }
    },

    # Lab results
    'lab_results': {
        'last_test_date': '2024-08-15',
        'results': {
            'cholesterol_total': {'value': 195, 'unit': 'mg/dL', 'reference': '< 200'},
            'ldl_cholesterol': {'value': 120, 'unit': 'mg/dL', 'reference': '< 100'},
            'hdl_cholesterol': {'value': 52, 'unit': 'mg/dL', 'reference': '> 40'},
            'triglycerides': {'value': 115, 'unit': 'mg/dL', 'reference': '< 150'},
            'glucose_fasting': {'value': 98, 'unit': 'mg/dL', 'reference': '70-100'},
            'hba1c': {'value': 5.4, 'unit': '%', 'reference': '< 5.7'},
            'vitamin_d': {'value': 28, 'unit': 'ng/mL', 'reference': '30-100'}
        }
    }
}


# ============================================================================
# SAMPLE QUERIES FOR TESTING
# ============================================================================

SAMPLE_QUERIES = [
    "How has my sleep quality been over the past month? Are there any patterns I should be aware of?",

    "I want to improve my cardiovascular health. What do my heart rate and activity data suggest?",

    "My father has Type 2 diabetes. Based on my data, what's my risk and what should I do?",

    "I've been feeling more tired lately. Can you analyze my recent health data to help understand why?",

    "Help me create a realistic exercise plan that fits my current activity level and health profile.",

    "What does my recent lab work say about my cholesterol? Should I be concerned?",

    "I want to lose 10 pounds over the next 3 months. Can you help me set up a plan?",

    "How does my heart rate variability compare to healthy ranges? What does this mean for my stress levels?",
]


def get_mock_user_data() -> Dict[str, Any]:
    """
    Get complete mock user data for system initialization.

    Returns:
        Dictionary with all mock user data
    """
    return MOCK_USER_DATA


def get_sample_queries() -> List[str]:
    """
    Get list of sample queries for testing.

    Returns:
        List of sample health queries
    """
    return SAMPLE_QUERIES


def print_data_summary():
    """Print a summary of the mock data for reference."""
    print("=" * 80)
    print("MOCK USER DATA SUMMARY")
    print("=" * 80)

    print("\n📊 USER PROFILE")
    print(f"  Age: {MOCK_USER_DATA['user_profile']['age']}")
    print(f"  Gender: {MOCK_USER_DATA['user_profile']['gender']}")
    print(f"  Height: {MOCK_USER_DATA['user_profile']['height_cm']} cm")
    print(f"  Weight: {MOCK_USER_DATA['user_profile']['weight_kg']} kg")

    print("\n🏥 HEALTH CONDITIONS")
    for condition in MOCK_USER_DATA['health_context']['health_records']['conditions']:
        print(f"  - {condition['name']} ({condition['status']})")

    print("\n💊 MEDICATIONS")
    for med in MOCK_USER_DATA['health_context']['health_records']['medications']:
        print(f"  - {med['name']} ({med['dosage']}, {med['frequency']})")

    print("\n⌚ WEARABLE DATA (30 days)")
    hr_data = MOCK_USER_DATA['personal_data']['wearable_data']['heart_rate']
    print(f"  - Heart Rate: {len(hr_data)} measurements")

    sleep_data = MOCK_USER_DATA['personal_data']['wearable_data']['sleep']
    print(f"  - Sleep: {len(sleep_data)} nights")

    activity_data = MOCK_USER_DATA['personal_data']['wearable_data']['activity']
    print(f"  - Activity: {len(activity_data)} days")

    print("\n🧪 LAB RESULTS")
    print(f"  Last test: {MOCK_USER_DATA['lab_results']['last_test_date']}")
    for test, result in MOCK_USER_DATA['lab_results']['results'].items():
        print(f"  - {test}: {result['value']} {result['unit']} (ref: {result['reference']})")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_data_summary()

    print("\n\n📝 SAMPLE QUERIES")
    print("=" * 80)
    for i, query in enumerate(SAMPLE_QUERIES, 1):
        print(f"\n{i}. {query}")
    print("\n" + "=" * 80)
