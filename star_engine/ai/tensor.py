"""
Star AI Engine — Universal Tensor & Autograd Computation Graph
Authoritative Reference: STAR_AI_SPEC.md

Features:
- N-dimensional tensor math with zero external dependencies
- Reverse-mode automatic differentiation (Autograd Engine)
- Matrix multiplication, broadcasting, activations (ReLU, Sigmoid, Tanh, GELU, Softmax)
- Topological sort gradient backpropagation
"""

import math
import random
from typing import List, Tuple, Union, Optional, Callable, Set, Any
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, to_star_value
)


def _flatten(nested: Any) -> List[float]:
    res = []
    if isinstance(nested, (int, float)):
        return [float(nested)]
    for item in nested:
        if isinstance(item, (list, tuple)):
            res.extend(_flatten(item))
        elif hasattr(item, "value"):
            res.append(float(item.value))
        else:
            res.append(float(item))
    return res


def _get_shape(nested: Any) -> Tuple[int, ...]:
    if isinstance(nested, (int, float)):
        return ()
    if not isinstance(nested, (list, tuple)) or len(nested) == 0:
        return (0,)
    if isinstance(nested[0], (list, tuple)):
        inner = _get_shape(nested[0])
        return (len(nested),) + inner
    return (len(nested),)


class Tensor:
    def __init__(self, data: Any, shape: Optional[Tuple[int, ...]] = None, requires_grad: bool = False, _children: Tuple["Tensor", ...] = ()):
        if isinstance(data, Tensor):
            self.data = list(data.data)
            self.shape = data.shape
        elif isinstance(data, (int, float)):
            self.data = [float(data)]
            self.shape = shape or (1,)
        else:
            self.data = _flatten(data)
            self.shape = shape or _get_shape(data)

        self.requires_grad = requires_grad
        self.grad: Optional[List[float]] = [0.0] * len(self.data) if requires_grad else None
        self._backward: Callable[[], None] = lambda: None
        self._prev: Set[Tensor] = set(_children)

    @classmethod
    def zeros(cls, shape: Tuple[int, ...], requires_grad: bool = False) -> "Tensor":
        size = 1
        for dim in shape:
            size *= dim
        t = cls([0.0] * size, shape=shape, requires_grad=requires_grad)
        return t

    @classmethod
    def ones(cls, shape: Tuple[int, ...], requires_grad: bool = False) -> "Tensor":
        size = 1
        for dim in shape:
            size *= dim
        return cls([1.0] * size, shape=shape, requires_grad=requires_grad)

    @classmethod
    def randn(cls, shape: Tuple[int, ...], mean: float = 0.0, std: float = 1.0, requires_grad: bool = False) -> "Tensor":
        size = 1
        for dim in shape:
            size *= dim
        # Box-Muller transform for normal distribution
        vals = []
        for _ in range(size):
            u1 = max(random.random(), 1e-12)
            u2 = random.random()
            z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            vals.append(mean + z * std)
        return cls(vals, shape=shape, requires_grad=requires_grad)

    @classmethod
    def xavier(cls, in_features: int, out_features: int, requires_grad: bool = True) -> "Tensor":
        std = math.sqrt(2.0 / (in_features + out_features))
        return cls.randn((in_features, out_features), mean=0.0, std=std, requires_grad=requires_grad)

    def zero_grad(self):
        if self.grad is not None:
            self.grad = [0.0] * len(self.data)

    def item(self) -> float:
        if len(self.data) == 1:
            return self.data[0]
        raise ValueError("Tensor.item() only valid for scalar tensors (size 1).")

    # --- Element-wise Operations ---

    def add(self, other: Union["Tensor", float, int]) -> "Tensor":
        other_t = other if isinstance(other, Tensor) else Tensor(other)
        out_data = []
        # Support broadcasting scalar or matching shapes
        if len(other_t.data) == 1:
            val = other_t.data[0]
            out_data = [a + val for a in self.data]
            out_shape = self.shape
        elif len(self.data) == 1:
            val = self.data[0]
            out_data = [val + b for b in other_t.data]
            out_shape = other_t.shape
        elif len(self.data) == len(other_t.data):
            out_data = [a + b for a, b in zip(self.data, other_t.data)]
            out_shape = self.shape
        else:
            # Row broadcasting (e.g., [batch, cols] + [cols])
            cols = self.shape[-1]
            out_data = [a + other_t.data[i % cols] for i, a in enumerate(self.data)]
            out_shape = self.shape

        req_grad = self.requires_grad or other_t.requires_grad
        out = Tensor(out_data, shape=out_shape, requires_grad=req_grad, _children=(self, other_t))

        def _backward():
            if self.requires_grad:
                if len(self.data) == len(out.grad):
                    for i in range(len(self.data)):
                        self.grad[i] += out.grad[i]
                else:
                    s = sum(out.grad)
                    for i in range(len(self.data)):
                        self.grad[i] += s / len(self.data)
            if other_t.requires_grad:
                if len(other_t.data) == len(out.grad):
                    for i in range(len(other_t.data)):
                        other_t.grad[i] += out.grad[i]
                elif len(other_t.data) == self.shape[-1]:
                    # Row broadcast gradient sum
                    cols = self.shape[-1]
                    for i, g in enumerate(out.grad):
                        other_t.grad[i % cols] += g
                else:
                    s = sum(out.grad)
                    for i in range(len(other_t.data)):
                        other_t.grad[i] += s / len(other_t.data)

        out._backward = _backward
        return out

    def sub(self, other: Union["Tensor", float, int]) -> "Tensor":
        other_t = other if isinstance(other, Tensor) else Tensor(other)
        return self.add(other_t.mul(-1.0))

    def mul(self, other: Union["Tensor", float, int]) -> "Tensor":
        other_t = other if isinstance(other, Tensor) else Tensor(other)
        out_data = []
        if len(other_t.data) == 1:
            val = other_t.data[0]
            out_data = [a * val for a in self.data]
            out_shape = self.shape
        elif len(self.data) == 1:
            val = self.data[0]
            out_data = [val * b for b in other_t.data]
            out_shape = other_t.shape
        elif len(self.data) == len(other_t.data):
            out_data = [a * b for a, b in zip(self.data, other_t.data)]
            out_shape = self.shape
        else:
            # Row broadcasting (e.g., [batch, cols] * [cols])
            cols = self.shape[-1]
            out_data = [a * other_t.data[i % cols] for i, a in enumerate(self.data)]
            out_shape = self.shape

        req_grad = self.requires_grad or other_t.requires_grad
        out = Tensor(out_data, shape=out_shape, requires_grad=req_grad, _children=(self, other_t))

        def _backward():
            if self.requires_grad:
                if len(other_t.data) == 1:
                    for i in range(len(self.data)):
                        self.grad[i] += other_t.data[0] * out.grad[i]
                elif len(other_t.data) == len(self.data):
                    for i in range(len(self.data)):
                        self.grad[i] += other_t.data[i] * out.grad[i]
                elif len(other_t.data) == self.shape[-1]:
                    cols = self.shape[-1]
                    for i in range(len(self.data)):
                        self.grad[i] += other_t.data[i % cols] * out.grad[i]
                else:
                    for i in range(len(self.data)):
                        self.grad[i] += out.grad[i]
            if other_t.requires_grad:
                if len(self.data) == 1:
                    for i in range(len(other_t.data)):
                        other_t.grad[i] += self.data[0] * out.grad[i]
                elif len(other_t.data) == len(self.data):
                    for i in range(len(other_t.data)):
                        other_t.grad[i] += self.data[i] * out.grad[i]
                elif len(other_t.data) == self.shape[-1]:
                    cols = self.shape[-1]
                    for i, g in enumerate(out.grad):
                        other_t.grad[i % cols] += self.data[i] * g
                else:
                    s = sum(out.grad)
                    for i in range(len(other_t.data)):
                        other_t.grad[i] += s / len(other_t.data)

        out._backward = _backward
        return out

    # --- Matrix Multiplication ---

    def matmul(self, other: "Tensor") -> "Tensor":
        if len(self.shape) != 2 or len(other.shape) != 2:
            raise ValueError(f"Matrix multiplication expects 2D tensors, got {self.shape} and {other.shape}")
        r1, c1 = self.shape
        r2, c2 = other.shape
        if c1 != r2:
            raise ValueError(f"Shape mismatch for matmul: ({r1}, {c1}) and ({r2}, {c2})")

        out_data = [0.0] * (r1 * c2)
        for i in range(r1):
            for j in range(c2):
                acc = 0.0
                for k in range(c1):
                    acc += self.data[i * c1 + k] * other.data[k * c2 + j]
                out_data[i * c2 + j] = acc

        req_grad = self.requires_grad or other.requires_grad
        out = Tensor(out_data, shape=(r1, c2), requires_grad=req_grad, _children=(self, other))

        def _backward():
            if self.requires_grad:
                # grad_self = out.grad @ other.T
                for i in range(r1):
                    for k in range(c1):
                        g = 0.0
                        for j in range(c2):
                            g += out.grad[i * c2 + j] * other.data[k * c2 + j]
                        self.grad[i * c1 + k] += g
            if other.requires_grad:
                # grad_other = self.T @ out.grad
                for k in range(c1):
                    for j in range(c2):
                        g = 0.0
                        for i in range(r1):
                            g += self.data[i * c1 + k] * out.grad[i * c2 + j]
                        other.grad[k * c2 + j] += g

        out._backward = _backward
        return out

    def transpose(self) -> "Tensor":
        if len(self.shape) != 2:
            return Tensor(self.data, shape=self.shape, requires_grad=self.requires_grad)
        rows, cols = self.shape
        out_data = [0.0] * (rows * cols)
        for r in range(rows):
            for c in range(cols):
                out_data[c * rows + r] = self.data[r * cols + c]
        out = Tensor(out_data, shape=(cols, rows), requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                for r in range(rows):
                    for c in range(cols):
                        self.grad[r * cols + c] += out.grad[c * rows + r]
        out._backward = _backward
        return out

    # --- Non-linear Activations ---

    def relu(self) -> "Tensor":
        out_data = [max(0.0, x) for x in self.data]
        out = Tensor(out_data, shape=self.shape, requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                for i, x in enumerate(self.data):
                    self.grad[i] += (out.grad[i] if x > 0 else 0.0)
        out._backward = _backward
        return out

    def sigmoid(self) -> "Tensor":
        out_data = [1.0 / (1.0 + math.exp(-max(min(x, 50.0), -50.0))) for x in self.data]
        out = Tensor(out_data, shape=self.shape, requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                for i, s in enumerate(out.data):
                    self.grad[i] += out.grad[i] * s * (1.0 - s)
        out._backward = _backward
        return out

    def tanh(self) -> "Tensor":
        out_data = [math.tanh(max(min(x, 50.0), -50.0)) for x in self.data]
        out = Tensor(out_data, shape=self.shape, requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                for i, t in enumerate(out.data):
                    self.grad[i] += out.grad[i] * (1.0 - t * t)
        out._backward = _backward
        return out

    def gelu(self) -> "Tensor":
        # Gaussian Error Linear Unit approximation
        out_data = []
        c = math.sqrt(2.0 / math.pi)
        for x in self.data:
            inner = c * (x + 0.044715 * (x ** 3))
            val = 0.5 * x * (1.0 + math.tanh(inner))
            out_data.append(val)
        out = Tensor(out_data, shape=self.shape, requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                for i, x in enumerate(self.data):
                    # Numerical gradient step for stability
                    h = 1e-5
                    inner1 = c * ((x + h) + 0.044715 * ((x + h) ** 3))
                    inner2 = c * ((x - h) + 0.044715 * ((x - h) ** 3))
                    f1 = 0.5 * (x + h) * (1.0 + math.tanh(inner1))
                    f2 = 0.5 * (x - h) * (1.0 + math.tanh(inner2))
                    df = (f1 - f2) / (2.0 * h)
                    self.grad[i] += out.grad[i] * df
        out._backward = _backward
        return out

    def softmax(self, dim: int = -1) -> "Tensor":
        if len(self.shape) != 2:
            max_val = max(self.data)
            exps = [math.exp(x - max_val) for x in self.data]
            s = sum(exps)
            return Tensor([e / s for e in exps], shape=self.shape, requires_grad=self.requires_grad)

        rows, cols = self.shape
        out_data = [0.0] * (rows * cols)
        for r in range(rows):
            row_vals = self.data[r * cols:(r + 1) * cols]
            max_v = max(row_vals)
            exps = [math.exp(v - max_v) for v in row_vals]
            s = sum(exps)
            for c_idx, e in enumerate(exps):
                out_data[r * cols + c_idx] = e / s
        return Tensor(out_data, shape=self.shape, requires_grad=self.requires_grad)

    # --- Reductions ---

    def sum(self) -> "Tensor":
        out = Tensor([sum(self.data)], shape=(1,), requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                g = out.grad[0]
                for i in range(len(self.data)):
                    self.grad[i] += g
        out._backward = _backward
        return out

    def mean(self) -> "Tensor":
        n = max(len(self.data), 1)
        out = Tensor([sum(self.data) / n], shape=(1,), requires_grad=self.requires_grad, _children=(self,))
        def _backward():
            if self.requires_grad:
                g = out.grad[0] / n
                for i in range(len(self.data)):
                    self.grad[i] += g
        out._backward = _backward
        return out

    # --- Reverse-Mode Automatic Differentiation ---

    def backward(self):
        topo: List[Tensor] = []
        visited: Set[Tensor] = set()

        def build_topo(v: Tensor):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        if self.grad is None:
            self.grad = [1.0] * len(self.data)
        else:
            self.grad = [1.0] * len(self.data)

        for node in reversed(topo):
            node._backward()

    def to_list(self) -> Any:
        if len(self.shape) == 1:
            return list(self.data)
        if len(self.shape) == 2:
            r, c = self.shape
            return [self.data[i * c:(i + 1) * c] for i in range(r)]
        return list(self.data)

    def __repr__(self) -> str:
        preview = str(self.to_list())
        if len(preview) > 50:
            preview = preview[:47] + "...]"
        return f"Tensor(shape={self.shape}, data={preview})"


class StarTensor(StarValue):
    def __init__(self, tensor: Tensor):
        self.tensor = tensor

    @property
    def type_name(self) -> str:
        return "Tensor"

    def get(self, name: str) -> StarValue:
        if name == "shape":
            return StarList([StarInteger(s) for s in self.tensor.shape])
        if name == "data":
            return to_star_value(self.tensor.to_list())
        if name == "item":
            return StarBuiltinFunction("item", lambda *a: StarDecimal(self.tensor.item()))

        if name == "add":
            def _add(*args):
                other = args[0].tensor if isinstance(args[0], StarTensor) else (args[0].value if hasattr(args[0], "value") else float(args[0]))
                return StarTensor(self.tensor.add(other))
            return StarBuiltinFunction("add", _add)

        if name == "sub":
            def _sub(*args):
                other = args[0].tensor if isinstance(args[0], StarTensor) else (args[0].value if hasattr(args[0], "value") else float(args[0]))
                return StarTensor(self.tensor.sub(other))
            return StarBuiltinFunction("sub", _sub)

        if name == "mul":
            def _mul(*args):
                other = args[0].tensor if isinstance(args[0], StarTensor) else (args[0].value if hasattr(args[0], "value") else float(args[0]))
                return StarTensor(self.tensor.mul(other))
            return StarBuiltinFunction("mul", _mul)

        if name == "matmul":
            def _mm(*args):
                if not isinstance(args[0], StarTensor):
                    raise TypeError("matmul requires a StarTensor argument")
                return StarTensor(self.tensor.matmul(args[0].tensor))
            return StarBuiltinFunction("matmul", _mm)

        if name in ("transpose", "t"):
            return StarBuiltinFunction("transpose", lambda *a: StarTensor(self.tensor.transpose()))

        if name == "relu":
            return StarBuiltinFunction("relu", lambda *a: StarTensor(self.tensor.relu()))
        if name == "sigmoid":
            return StarBuiltinFunction("sigmoid", lambda *a: StarTensor(self.tensor.sigmoid()))
        if name == "tanh":
            return StarBuiltinFunction("tanh", lambda *a: StarTensor(self.tensor.tanh()))
        if name == "gelu":
            return StarBuiltinFunction("gelu", lambda *a: StarTensor(self.tensor.gelu()))
        if name == "softmax":
            return StarBuiltinFunction("softmax", lambda *a: StarTensor(self.tensor.softmax()))

        if name == "sum":
            return StarBuiltinFunction("sum", lambda *a: StarTensor(self.tensor.sum()))
        if name == "mean":
            return StarBuiltinFunction("mean", lambda *a: StarTensor(self.tensor.mean()))
        if name == "backward":
            return StarBuiltinFunction("backward", lambda *a: self.tensor.backward() or StarNull())
        if name == "zero_grad":
            return StarBuiltinFunction("zero_grad", lambda *a: self.tensor.zero_grad() or StarNull())

        from star_engine.errors import StarNameError
        raise StarNameError(f"Tensor has no member '{name}'.")

    def to_string(self) -> str:
        return repr(self.tensor)

    def __repr__(self) -> str:
        return self.to_string()
