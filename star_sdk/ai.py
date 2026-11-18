"""
Star Standard Library — AI, Deep Learning & Autonomous Agent Subsystem (use AI)
Authoritative Reference: STAR_AI_SPEC.md

Exports the AI, Neural, and Tensor modules into Star Language programs.
"""

from typing import Dict, Any, List, Optional
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, StarModule, to_star_value
)
from star_engine.ai.tensor import Tensor, StarTensor
from star_engine.ai.nn import (
    Dense, Sequential, LayerNorm, SelfAttention, TransformerBlock, StarModelWrapper
)
from star_engine.ai.loss import (
    MSELoss, CrossEntropyLoss, BinaryCrossEntropyLoss, StarLossWrapper
)
from star_engine.ai.optim import (
    SGD, Adam, AdamW, StarOptimizerWrapper
)
from star_engine.ai.agent import (
    VectorStore, StarVectorStore, AIAgent, StarAIAgentWrapper, cosine_similarity
)


def _to_native_list(val: Any) -> Any:
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, (StarInteger, StarDecimal)):
        return float(val.value)
    if isinstance(val, StarList):
        return [_to_native_list(x) for x in val.elements]
    if isinstance(val, (list, tuple)):
        return [_to_native_list(x) for x in val]
    return float(val)


def create_ai_module() -> StarModule:
    exports: Dict[str, StarValue] = {}

    # 1. Tensor Factory Functions
    def _create_tensor(*args: StarValue) -> StarValue:
        if not args:
            return StarTensor(Tensor([0.0]))
        data = _to_native_list(args[0])
        shape = None
        req_grad = False
        if len(args) > 1 and isinstance(args[1], StarList):
            shape = tuple(int(s.value) for s in args[1].elements)
        if len(args) > 2 and hasattr(args[2], "value"):
            req_grad = bool(args[2].value)
        return StarTensor(Tensor(data, shape=shape, requires_grad=req_grad))
    exports["tensor"] = StarBuiltinFunction("tensor", _create_tensor)

    def _zeros(*args: StarValue) -> StarValue:
        if not args:
            return StarTensor(Tensor.zeros((1,)))
        shape = tuple(int(s.value if hasattr(s, "value") else s) for s in (args[0].elements if hasattr(args[0], "elements") else args))
        req_grad = bool(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else False
        return StarTensor(Tensor.zeros(shape, requires_grad=req_grad))
    exports["zeros"] = StarBuiltinFunction("zeros", _zeros)

    def _ones(*args: StarValue) -> StarValue:
        if not args:
            return StarTensor(Tensor.ones((1,)))
        shape = tuple(int(s.value if hasattr(s, "value") else s) for s in (args[0].elements if hasattr(args[0], "elements") else args))
        req_grad = bool(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else False
        return StarTensor(Tensor.ones(shape, requires_grad=req_grad))
    exports["ones"] = StarBuiltinFunction("ones", _ones)

    def _randn(*args: StarValue) -> StarValue:
        if not args:
            return StarTensor(Tensor.randn((1,)))
        shape = tuple(int(s.value if hasattr(s, "value") else s) for s in (args[0].elements if hasattr(args[0], "elements") else args))
        req_grad = bool(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else False
        return StarTensor(Tensor.randn(shape, requires_grad=req_grad))
    exports["randn"] = StarBuiltinFunction("randn", _randn)

    # 2. Neural Network Layers
    def _dense(*args: StarValue) -> StarValue:
        if len(args) < 2:
            raise ValueError("Dense requires (in_features, out_features)")
        in_f = int(args[0].value)
        out_f = int(args[1].value)
        act = args[2].to_string() if len(args) > 2 else None
        return StarModelWrapper(Dense(in_f, out_f, activation=act))
    exports["Dense"] = StarBuiltinFunction("Dense", _dense)

    def _sequential(*args: StarValue) -> StarValue:
        layers = []
        if args and isinstance(args[0], StarList):
            for item in args[0].elements:
                if isinstance(item, StarModelWrapper):
                    layers.append(item.module)
        return StarModelWrapper(Sequential(layers))
    exports["Sequential"] = StarBuiltinFunction("Sequential", _sequential)

    def _layer_norm(*args: StarValue) -> StarValue:
        dim = int(args[0].value) if args else 64
        return StarModelWrapper(LayerNorm(dim))
    exports["LayerNorm"] = StarBuiltinFunction("LayerNorm", _layer_norm)

    def _self_attention(*args: StarValue) -> StarValue:
        dim = int(args[0].value) if args else 64
        return StarModelWrapper(SelfAttention(dim))
    exports["SelfAttention"] = StarBuiltinFunction("SelfAttention", _self_attention)

    def _transformer_block(*args: StarValue) -> StarValue:
        dim = int(args[0].value) if args else 64
        ffn = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else None
        return StarModelWrapper(TransformerBlock(dim, ffn_dim=ffn))
    exports["TransformerBlock"] = StarBuiltinFunction("TransformerBlock", _transformer_block)

    # 3. Loss Functions
    exports["MSELoss"] = StarBuiltinFunction("MSELoss", lambda *a: StarLossWrapper(MSELoss()))
    exports["CrossEntropyLoss"] = StarBuiltinFunction("CrossEntropyLoss", lambda *a: StarLossWrapper(CrossEntropyLoss()))
    exports["BinaryCrossEntropyLoss"] = StarBuiltinFunction("BinaryCrossEntropyLoss", lambda *a: StarLossWrapper(BinaryCrossEntropyLoss()))

    # 4. Optimizers
    def _adam(*args: StarValue) -> StarValue:
        if not args:
            raise ValueError("Adam requires (parameters, lr=0.001)")
        raw_params = []
        if isinstance(args[0], StarList):
            raw_params = [p.tensor for p in args[0].elements if isinstance(p, StarTensor)]
        elif isinstance(args[0], StarModelWrapper):
            raw_params = args[0].module.parameters()
        lr = float(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0.001
        return StarOptimizerWrapper(Adam(raw_params, lr=lr))
    exports["Adam"] = StarBuiltinFunction("Adam", _adam)

    def _sgd(*args: StarValue) -> StarValue:
        if not args:
            raise ValueError("SGD requires (parameters, lr=0.01)")
        raw_params = []
        if isinstance(args[0], StarList):
            raw_params = [p.tensor for p in args[0].elements if isinstance(p, StarTensor)]
        elif isinstance(args[0], StarModelWrapper):
            raw_params = args[0].module.parameters()
        lr = float(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 0.01
        mom = float(args[2].value) if len(args) > 2 and hasattr(args[2], "value") else 0.0
        return StarOptimizerWrapper(SGD(raw_params, lr=lr, momentum=mom))
    exports["SGD"] = StarBuiltinFunction("SGD", _sgd)

    # 5. Vector Store & Autonomous Agent
    def _vector_store(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "default"
        return StarVectorStore(VectorStore(name))
    exports["VectorStore"] = StarBuiltinFunction("VectorStore", _vector_store)

    def _agent(*args: StarValue) -> StarValue:
        name = args[0].to_string() if args else "StarAgent"
        sys_prompt = args[1].to_string() if len(args) > 1 else "You are an autonomous Star AI Agent."
        return StarAIAgentWrapper(AIAgent(name, system_prompt=sys_prompt))
    exports["Agent"] = StarBuiltinFunction("Agent", _agent)

    def _cosine_sim(*args: StarValue) -> StarValue:
        if len(args) < 2:
            return StarDecimal(0.0)
        v1 = [float(x.value if hasattr(x, "value") else x) for x in (args[0].elements if hasattr(args[0], "elements") else args[0])]
        v2 = [float(x.value if hasattr(x, "value") else x) for x in (args[1].elements if hasattr(args[1], "elements") else args[1])]
        return StarDecimal(cosine_similarity(v1, v2))
    exports["cosine_similarity"] = StarBuiltinFunction("cosine_similarity", _cosine_sim)

    return StarModule("AI", exports)
