"""
Base agent wrapper for the Agent-Based Commerce Platform.
Provides a common interface for all shopping agents (fashion stylist, beauty consultant, etc.)
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all shopping agents.
    Defines the common interface that all agents must implement.
    """

    def __init__(self, agent_id: str, name: str, version: str = "1.0.0"):
        """
        Initialize the base agent.

        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name of the agent
            version: Version of the agent
        """
        self.agent_id = agent_id
        self.name = name
        self.version = version
        self.created_at = datetime.utcnow()
        logger.info(f"Initialized agent {self.agent_id}: {self.name} v{self.version}")

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return agent output.
        This method must be implemented by all concrete agents.

        Args:
            input_data: Input data conforming to the agent's input schema

        Returns:
            Output data conforming to the agent's output schema
        """
        pass

    @abstractmethod
    def get_input_schema(self) -> Dict[str, Any]:
        """
        Return the JSON schema for agent input validation.

        Returns:
            JSON schema dictionary
        """
        pass

    @abstractmethod
    def get_output_schema(self) -> Dict[str, Any]:
        """
        Return the JSON schema for agent output validation.

        Returns:
            JSON schema dictionary
        """
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data against the agent's input schema.
        Basic implementation - can be extended with jsonschema library.

        Args:
            input_data: Input data to validate

        Returns:
            True if valid, False otherwise
        """
        # Basic validation - in production, use jsonschema library
        try:
            input_schema = self.get_input_schema()
            # For now, just check if it's a dict
            return isinstance(input_data, dict)
        except Exception as e:
            logger.error(f"Error validating input: {e}")
            return False

    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """
        Validate output data against the agent's output schema.

        Args:
            output_data: Output data to validate

        Returns:
            True if valid, False otherwise
        """
        # Basic validation - in production, use jsonschema library
        try:
            output_schema = self.get_output_schema()
            # For now, just check if it's a dict
            return isinstance(output_data, dict)
        except Exception as e:
            logger.error(f"Error validating output: {e}")
            return False

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about this agent.

        Returns:
            Dictionary containing agent metadata
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "input_schema": self.get_input_schema(),
            "output_schema": self.get_output_schema()
        }

    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the agent.

        Returns:
            Dictionary containing health status
        """
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }


# Example concrete agent implementation
class FashionStylistAgent(BaseAgent):
    """
    Example implementation of a fashion stylist agent.
    Provides clothing and outfit recommendations based on user preferences.
    """

    def __init__(self):
        super().__init__(
            agent_id="fashion_stylist_v1",
            name="Fashion Stylist Agent",
            version="1.0.0"
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process fashion styling requests.

        Expected input:
        {
            "user_preferences": {
                "style": "casual|formal|trendy|classic",
                "occasion": "work|party|date|casual",
                "body_type": "string",
                "color_preferences": ["string"],
                "budget_range": {"min": number, "max": number}
            },
            "context": {
                "season": "spring|summer|fall|winter",
                "weather": "string"
            }
        }

        Returns:
        {
            "recommendations": [
                {
                    "item_id": "string",
                    "name": "string",
                    "category": "top|bottom|shoes|accessories",
                    "brand": "string",
                    "price": number,
                    "match_score": number (0-1),
                    "reasoning": "string"
                }
            ],
            "outfit_score": number (0-1),
            "styling_tips": ["string"]
        }
        """
        logger.info(f"Processing fashion styling request: {input_data}")

        # Placeholder implementation - in reality, this would call LLMs, access product databases, etc.
        user_prefs = input_data.get("user_preferences", {})
        context = input_data.get("context", {})

        # Mock recommendations based on input
        recommendations = [
            {
                "item_id": "top_001",
                "name": "Casual Cotton T-Shirt",
                "category": "top",
                "brand": "StyleLab",
                "price": 29.99,
                "match_score": 0.85,
                "reasoning": "Matches your casual style preference and budget"
            },
            {
                "item_id": "bottom_001",
                "name": "Denim Jeans",
                "category": "bottom",
                "brand": "DenimCo",
                "price": 59.99,
                "match_score": 0.9,
                "reasoning": "Classic choice for casual occasions"
            }
        ]

        return {
            "recommendations": recommendations,
            "outfit_score": 0.88,
            "styling_tips": [
                "Add a light jacket for cooler evenings",
                "Consider sneakers for comfort"
            ]
        }

    def get_input_schema(self) -> Dict[str, Any]:
        """Return JSON schema for fashion stylist agent input."""
        return {
            "type": "object",
            "properties": {
                "user_preferences": {
                    "type": "object",
                    "properties": {
                        "style": {"type": "string", "enum": ["casual", "formal", "trendy", "classic"]},
                        "occasion": {"type": "string", "enum": ["work", "party", "date", "casual"]},
                        "body_type": {"type": "string"},
                        "color_preferences": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "budget_range": {
                            "type": "object",
                            "properties": {
                                "min": {"type": "number", "minimum": 0},
                                "max": {"type": "number", "minimum": 0}
                            },
                            "required": ["min", "max"]
                        }
                    },
                    "required": ["style", "occasion"]
                },
                "context": {
                    "type": "object",
                    "properties": {
                        "season": {"type": "string", "enum": ["spring", "summer", "fall", "winter"]},
                        "weather": {"type": "string"}
                    }
                }
            },
            "required": ["user_preferences"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return JSON schema for fashion stylist agent output."""
        return {
            "type": "object",
            "properties": {
                "recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item_id": {"type": "string"},
                            "name": {"type": "string"},
                            "category": {"type": "string", "enum": ["top", "bottom", "shoes", "accessories"]},
                            "brand": {"type": "string"},
                            "price": {"type": "number", "minimum": 0},
                            "match_score": {"type": "number", "minimum": 0, "maximum": 1},
                            "reasoning": {"type": "string"}
                        },
                        "required": ["item_id", "name", "category", "brand", "price", "match_score", "reasoning"]
                    }
                },
                "outfit_score": {"type": "number", "minimum": 0, "maximum": 1},
                "styling_tips": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["recommendations", "outfit_score"]
        }