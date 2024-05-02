"""
The chatbot needs the capability to answer questions about wait time. However, our organization
does not store wait time data. We simulate the chatbot finding the current wait time at a
hospital and the hospital with the shortest wait time.    
"""

import os
import numpy as np
from langchain_community.graphs import Neo4jGraph
from typing import Any


def _get_current_hospitals():
    """Fetch a list of current hospital names from the database"""
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    current_hospitals = graph.query(
        """
        MATCH (h:Hospital)
        RETURN h.name AS hospital_name
        """
    )

    return [d["hospital_name"].lower() for d in current_hospitals]


def _get_current_wait_time_minutes(hospital: str) -> int:
    """Get current wait time at a hospital in minutes

    Args:
        hospital (str): hospital name to get wait times for

    Returns:
        int: wait time in minutes
    """
    current_hospitals = _get_current_hospitals()

    if hospital.lower() not in current_hospitals:
        return -1

    return np.random.randint(low=0, high=600)


def get_current_wait_times(hospital: str) -> str:
    """Return formatted current wait time at a hospital."""
    wait_time_in_minutes = _get_current_wait_time_minutes(hospital)

    if wait_time_in_minutes == -1:
        return f"Hospital {hospital} does not exist in the database."

    hours, minutes = divmod(wait_time_in_minutes, 60)

    if hours > 0:
        return f"{hours} hours {minutes} minutes"
    else:
        return f"{minutes} minutes"


# We have to provide a throwaway input _ as the agent is designed to pass input into functions
def get_shortest_wait_hospital(_: Any) -> dict[str, float]:
    """Finds the hospital with the shortest wait time (simulated)."""
    current_hospitals = _get_current_hospitals()

    current_wait_times = [
        _get_current_wait_time_minutes(hospital) for hospital in current_hospitals
    ]

    shortest_wait_idx = np.argmin(current_wait_times)
    shortest_wait_hospital = current_hospitals[shortest_wait_idx]
    shortest_wait_time = current_wait_times[shortest_wait_idx]

    return {shortest_wait_hospital: shortest_wait_time}
