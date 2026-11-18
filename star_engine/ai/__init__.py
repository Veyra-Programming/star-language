"""
Star AI & Neural Computation Engine
Authoritative Reference: STAR_AI_SPEC.md

Exports:
- Tensor, StarTensor
- Dense, Sequential, LayerNorm, SelfAttention, TransformerBlock, StarModelWrapper
- MSELoss, CrossEntropyLoss, BinaryCrossEntropyLoss, StarLossWrapper
- SGD, Adam, AdamW, StarOptimizerWrapper
- VectorStore, StarVectorStore, AIAgent, StarAIAgentWrapper, cosine_similarity
"""

from star_engine.ai.tensor import Tensor, StarTensor
from star_engine.ai.nn import (
    Module, Dense, Sequential, LayerNorm, SelfAttention, TransformerBlock, StarModelWrapper
)
from star_engine.ai.loss import (
    MSELoss, CrossEntropyLoss, BinaryCrossEntropyLoss, StarLossWrapper
)
from star_engine.ai.optim import (
    Optimizer, SGD, Adam, AdamW, StarOptimizerWrapper
)
from star_engine.ai.agent import (
    VectorStore, StarVectorStore, AIAgent, StarAIAgentWrapper, cosine_similarity
)

__version__ = "1.3.0"
__all__ = [
    "Tensor", "StarTensor",
    "Module", "Dense", "Sequential", "LayerNorm", "SelfAttention", "TransformerBlock", "StarModelWrapper",
    "MSELoss", "CrossEntropyLoss", "BinaryCrossEntropyLoss", "StarLossWrapper",
    "Optimizer", "SGD", "Adam", "AdamW", "StarOptimizerWrapper",
    "VectorStore", "StarVectorStore", "AIAgent", "StarAIAgentWrapper", "cosine_similarity"
]
