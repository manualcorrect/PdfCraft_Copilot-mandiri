"""
Description Training System for Bank Mandiri e-Statements
A dedicated model and validation framework for understanding, formatting,
and monitoring transaction descriptions according to official banking references.
"""

from .description_model import DescriptionModelEngine
from .syntax_rules import TransactionCategory, TransactionSyntaxRule

__all__ = ["DescriptionModelEngine", "TransactionCategory", "TransactionSyntaxRule"]
