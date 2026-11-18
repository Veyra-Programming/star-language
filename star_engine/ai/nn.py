"""
Star AI Engine — Neural Network Layer Modules & Model Architectures
Authoritative Reference: STAR_AI_SPEC.md

Features:
- Dense / Linear layers with Xavier initialization
- Sequential model containers
- Multi-Head Self-Attention & Transformer Blocks
- Layer Normalization & Dropout
- Parameter auto-collection and gradient zeroing
"""

import math
from typing import List, Optional, Any, Callable
from star_engine.ai.tensor import Tensor, StarTensor
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, to_star_value
)


class Module:
    def __init__(self):
        self._submodules: List["Module"] = []
        self._parameters: List[Tensor] = []

    def parameters(self) -> List[Tensor]:
        params = list(self._parameters)
        for sub in self._submodules:
            params.extend(sub.parameters())
        return params

    def zero_grad(self):
        for p in self.parameters():
            p.zero_grad()

    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError

    def __call__(self, x: Tensor) -> Tensor:
        return self.forward(x)


class Dense(Module):
    def __init__(self, in_features: int, out_features: int, activation: Optional[str] = None):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.activation = activation.lower() if activation else None

        self.weight = Tensor.xavier(in_features, out_features, requires_grad=True)
        self.bias = Tensor.zeros((1, out_features), requires_grad=True)
        self._parameters = [self.weight, self.bias]

    def forward(self, x: Tensor) -> Tensor:
        # y = x @ W + b
        out = x.matmul(self.weight).add(self.bias)
        if self.activation == "relu":
            return out.relu()
        elif self.activation == "sigmoid":
            return out.sigmoid()
        elif self.activation == "tanh":
            return out.tanh()
        elif self.activation == "gelu":
            return out.gelu()
        elif self.activation == "softmax":
            return out.softmax()
        return out


class Sequential(Module):
    def __init__(self, layers: List[Module]):
        super().__init__()
        self.layers = list(layers)
        self._submodules = list(layers)

    def forward(self, x: Tensor) -> Tensor:
        curr = x
        for layer in self.layers:
            curr = layer.forward(curr)
        return curr

    def add(self, layer: Module):
        self.layers.append(layer)
        self._submodules.append(layer)


class LayerNorm(Module):
    def __init__(self, normalized_shape: int, eps: float = 1e-5):
        super().__init__()
        self.eps = eps
        self.gamma = Tensor.ones((1, normalized_shape), requires_grad=True)
        self.beta = Tensor.zeros((1, normalized_shape), requires_grad=True)
        self._parameters = [self.gamma, self.beta]

    def forward(self, x: Tensor) -> Tensor:
        # Standardize features: (x - mean) / sqrt(var + eps) * gamma + beta
        mean = x.mean()
        diff = x.sub(mean)
        var = diff.mul(diff).mean()
        std = Tensor([math.sqrt(var.data[0] + self.eps)], shape=(1,))
        normed = diff.mul(Tensor([1.0 / std.data[0]], shape=(1,)))
        return normed.mul(self.gamma).add(self.beta)


class SelfAttention(Module):
    def __init__(self, embed_dim: int):
        super().__init__()
        self.embed_dim = embed_dim
        self.scale = 1.0 / math.sqrt(embed_dim)
        self.w_q = Dense(embed_dim, embed_dim)
        self.w_k = Dense(embed_dim, embed_dim)
        self.w_v = Dense(embed_dim, embed_dim)
        self.w_out = Dense(embed_dim, embed_dim)
        self._submodules = [self.w_q, self.w_k, self.w_v, self.w_out]

    def forward(self, x: Tensor) -> Tensor:
        # Q = x @ W_q, K = x @ W_k, V = x @ W_v
        Q = self.w_q.forward(x)
        K = self.w_k.forward(x)
        V = self.w_v.forward(x)
        
        # Attention scores = Softmax((Q @ K.T) / sqrt(d_k)) @ V
        scores = Q.matmul(K.transpose()).mul(self.scale)
        attn_weights = scores.softmax()
        context = attn_weights.matmul(V)
        return self.w_out.forward(context)


class TransformerBlock(Module):
    def __init__(self, embed_dim: int, ffn_dim: Optional[int] = None):
        super().__init__()
        ffn_dim = ffn_dim or embed_dim * 4
        self.attn = SelfAttention(embed_dim)
        self.norm1 = LayerNorm(embed_dim)
        self.ffn = Sequential([
            Dense(embed_dim, ffn_dim, activation="gelu"),
            Dense(ffn_dim, embed_dim)
        ])
        self.norm2 = LayerNorm(embed_dim)
        self._submodules = [self.attn, self.norm1, self.ffn, self.norm2]

    def forward(self, x: Tensor) -> Tensor:
        # Pre-LN Residual Transformer Architecture
        attn_out = self.attn.forward(self.norm1.forward(x))
        x = x.add(attn_out)
        ffn_out = self.ffn.forward(self.norm2.forward(x))
        return x.add(ffn_out)


class StarModelWrapper(StarValue):
    def __init__(self, module: Module):
        self.module = module

    @property
    def type_name(self) -> str:
        return "NeuralModel"

    def get(self, name: str) -> StarValue:
        if name in ("forward", "predict"):
            def _fwd(*args):
                if not args or not isinstance(args[0], StarTensor):
                    raise TypeError("forward expects a StarTensor")
                out_t = self.module.forward(args[0].tensor)
                return StarTensor(out_t)
            return StarBuiltinFunction(name, _fwd)

        if name == "zero_grad":
            def _zg(*args):
                self.module.zero_grad()
                return StarNull()
            return StarBuiltinFunction("zero_grad", _zg)

        if name == "parameters":
            def _params(*args):
                params = [StarTensor(p) for p in self.module.parameters()]
                return StarList(params)
            return StarBuiltinFunction("parameters", _params)

        from star_engine.errors import StarNameError
        raise StarNameError(f"NeuralModel has no member '{name}'.")

    def to_string(self) -> str:
        param_count = sum(len(p.data) for p in self.module.parameters())
        return f"<NeuralModel layers={len(getattr(self.module, 'layers', [1]))} parameters={param_count}>"

    def __repr__(self) -> str:
        return self.to_string()
