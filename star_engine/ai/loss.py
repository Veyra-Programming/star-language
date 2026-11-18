"""
Star AI Engine — Loss Functions & Objective Criteria
Authoritative Reference: STAR_AI_SPEC.md
"""

import math
from typing import Optional, Any
from star_engine.ai.tensor import Tensor, StarTensor
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, to_star_value
)


class MSELoss:
    def forward(self, pred: Tensor, target: Tensor) -> Tensor:
        diff = pred.sub(target)
        sq = diff.mul(diff)
        return sq.mean()

    def __call__(self, pred: Tensor, target: Tensor) -> Tensor:
        return self.forward(pred, target)


class BinaryCrossEntropyLoss:
    def __init__(self, eps: float = 1e-12):
        self.eps = eps

    def forward(self, pred: Tensor, target: Tensor) -> Tensor:
        # BCE = - [ y * log(p + eps) + (1 - y) * log(1 - p + eps) ]
        loss_data = []
        for p, y in zip(pred.data, target.data):
            p_clamped = max(min(p, 1.0 - self.eps), self.eps)
            val = -(y * math.log(p_clamped) + (1.0 - y) * math.log(1.0 - p_clamped))
            loss_data.append(val)

        out = Tensor([sum(loss_data) / max(len(loss_data), 1)], shape=(1,), requires_grad=True, _children=(pred,))
        def _backward():
            if pred.requires_grad:
                n = len(pred.data)
                for i in range(n):
                    p = max(min(pred.data[i], 1.0 - self.eps), self.eps)
                    y = target.data[i]
                    # dL/dp = (p - y) / (p * (1 - p))
                    grad = (p - y) / (p * (1.0 - p) * n)
                    pred.grad[i] += out.grad[0] * grad
        out._backward = _backward
        return out

    def __call__(self, pred: Tensor, target: Tensor) -> Tensor:
        return self.forward(pred, target)


class CrossEntropyLoss:
    def __init__(self, eps: float = 1e-12):
        self.eps = eps

    def forward(self, pred: Tensor, target: Tensor) -> Tensor:
        # Softmax + Negative Log Likelihood
        probs = pred.softmax()
        loss_data = []
        rows = pred.shape[0] if len(pred.shape) == 2 else 1
        cols = pred.shape[1] if len(pred.shape) == 2 else len(pred.data)

        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                y = target.data[idx]
                p = max(probs.data[idx], self.eps)
                loss_data.append(-y * math.log(p))

        out = Tensor([sum(loss_data) / max(rows, 1)], shape=(1,), requires_grad=True, _children=(pred,))
        def _backward():
            if pred.requires_grad:
                for i in range(len(pred.data)):
                    # Softmax + CrossEntropy derivative is simply (prob - target) / batch_size
                    grad = (probs.data[i] - target.data[i]) / max(rows, 1)
                    pred.grad[i] += out.grad[0] * grad
        out._backward = _backward
        return out


class StarLossWrapper(StarValue):
    def __init__(self, loss_fn: Any):
        self.loss_fn = loss_fn

    @property
    def type_name(self) -> str:
        return "LossFunction"

    def get(self, name: str) -> StarValue:
        if name in ("forward", "calculate", "call"):
            def _calc(*args):
                if len(args) < 2:
                    raise ValueError("Loss forward requires (pred, target)")
                pred = args[0].tensor if isinstance(args[0], StarTensor) else Tensor(args[0])
                target = args[1].tensor if isinstance(args[1], StarTensor) else Tensor(args[1])
                out = self.loss_fn.forward(pred, target)
                return StarTensor(out)
            return StarBuiltinFunction(name, _calc)

        from star_engine.errors import StarNameError
        raise StarNameError(f"LossFunction has no member '{name}'.")

    def to_string(self) -> str:
        return f"<{type(self.loss_fn).__name__}>"

    def __repr__(self) -> str:
        return self.to_string()
