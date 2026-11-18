"""
Star AI Engine — Optimizers & Parameter Updaters
Authoritative Reference: STAR_AI_SPEC.md

Features:
- Stochastic Gradient Descent (SGD) with momentum
- Adam (Adaptive Moment Estimation) optimizer
- AdamW (Decoupled Weight Decay) optimizer
"""

import math
from typing import List, Optional
from star_engine.ai.tensor import Tensor, StarTensor
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, to_star_value
)


class Optimizer:
    def __init__(self, params: List[Tensor], lr: float = 0.01):
        self.params = [p for p in params if p.requires_grad]
        self.lr = lr

    def zero_grad(self):
        for p in self.params:
            p.zero_grad()

    def step(self):
        raise NotImplementedError


class SGD(Optimizer):
    def __init__(self, params: List[Tensor], lr: float = 0.01, momentum: float = 0.0):
        super().__init__(params, lr=lr)
        self.momentum = momentum
        self.velocities: List[List[float]] = [[0.0] * len(p.data) for p in self.params]

    def step(self):
        for idx, p in enumerate(self.params):
            if p.grad is None:
                continue
            for i in range(len(p.data)):
                v = self.momentum * self.velocities[idx][i] + self.lr * p.grad[i]
                self.velocities[idx][i] = v
                p.data[i] -= v


class Adam(Optimizer):
    def __init__(self, params: List[Tensor], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        super().__init__(params, lr=lr)
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m: List[List[float]] = [[0.0] * len(p.data) for p in self.params]
        self.v: List[List[float]] = [[0.0] * len(p.data) for p in self.params]

    def step(self):
        self.t += 1
        b1_corr = 1.0 - (self.beta1 ** self.t)
        b2_corr = 1.0 - (self.beta2 ** self.t)

        for idx, p in enumerate(self.params):
            if p.grad is None:
                continue
            for i in range(len(p.data)):
                g = p.grad[i]
                # Update biased first moment
                self.m[idx][i] = self.beta1 * self.m[idx][i] + (1.0 - self.beta1) * g
                # Update biased second raw moment
                self.v[idx][i] = self.beta2 * self.v[idx][i] + (1.0 - self.beta2) * (g * g)

                # Compute bias-corrected estimates
                m_hat = self.m[idx][i] / b1_corr
                v_hat = self.v[idx][i] / b2_corr

                # Update parameter
                p.data[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.eps)


class AdamW(Adam):
    def __init__(self, params: List[Tensor], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8, weight_decay: float = 0.01):
        super().__init__(params, lr=lr, beta1=beta1, beta2=beta2, eps=eps)
        self.weight_decay = weight_decay

    def step(self):
        # Apply decoupled weight decay
        for p in self.params:
            for i in range(len(p.data)):
                p.data[i] -= self.lr * self.weight_decay * p.data[i]
        super().step()


class StarOptimizerWrapper(StarValue):
    def __init__(self, optimizer: Optimizer):
        self.optimizer = optimizer

    @property
    def type_name(self) -> str:
        return "Optimizer"

    def get(self, name: str) -> StarValue:
        if name == "step":
            def _step(*args):
                self.optimizer.step()
                return StarNull()
            return StarBuiltinFunction("step", _step)

        if name == "zero_grad":
            def _zg(*args):
                self.optimizer.zero_grad()
                return StarNull()
            return StarBuiltinFunction("zero_grad", _zg)

        if name == "lr":
            return StarDecimal(self.optimizer.lr)

        from star_engine.errors import StarNameError
        raise StarNameError(f"Optimizer has no member '{name}'.")

    def to_string(self) -> str:
        return f"<{type(self.optimizer).__name__} lr={self.optimizer.lr}>"

    def __repr__(self) -> str:
        return self.to_string()
