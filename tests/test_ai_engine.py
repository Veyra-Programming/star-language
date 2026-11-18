"""
Unit Tests for Star AI Engine, Universal Tensors, Autograd, Neural Layers & Agents
Authoritative Reference: STAR_AI_SPEC.md
"""

import unittest
import math
from star_engine.ai.tensor import Tensor, StarTensor
from star_engine.ai.nn import Dense, Sequential, LayerNorm, SelfAttention, TransformerBlock
from star_engine.ai.loss import MSELoss, BinaryCrossEntropyLoss, CrossEntropyLoss
from star_engine.ai.optim import SGD, Adam, AdamW
from star_engine.ai.agent import VectorStore, AIAgent, cosine_similarity
from star_sdk.ai import create_ai_module
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_engine.vm import StarVM


class TestTensorAndAutograd(unittest.TestCase):
    def test_tensor_creation_and_basic_ops(self):
        t1 = Tensor([1.0, 2.0, 3.0], shape=(3,), requires_grad=True)
        t2 = Tensor([4.0, 5.0, 6.0], shape=(3,), requires_grad=True)

        t_add = t1.add(t2)
        self.assertEqual(t_add.data, [5.0, 7.0, 9.0])

        t_mul = t1.mul(t2)
        self.assertEqual(t_mul.data, [4.0, 10.0, 18.0])

        out = t_mul.sum()
        out.backward()

        # d(t1 * t2)/dt1 = t2
        self.assertEqual(t1.grad, [4.0, 5.0, 6.0])
        # d(t1 * t2)/dt2 = t1
        self.assertEqual(t2.grad, [1.0, 2.0, 3.0])

    def test_matrix_multiplication_autograd(self):
        # A: (2, 3), B: (3, 2) -> C: (2, 2)
        A = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
        B = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], requires_grad=True)

        C = A.matmul(B)
        self.assertEqual(C.shape, (2, 2))
        self.assertEqual(C.data, [22.0, 28.0, 49.0, 64.0])

        loss = C.sum()
        loss.backward()

        self.assertIsNotNone(A.grad)
        self.assertIsNotNone(B.grad)
        self.assertEqual(len(A.grad), 6)
        self.assertEqual(len(B.grad), 6)

    def test_activations(self):
        t = Tensor([-2.0, 0.0, 2.0], requires_grad=True)
        relu_out = t.relu()
        self.assertEqual(relu_out.data, [0.0, 0.0, 2.0])

        sig_out = t.sigmoid()
        self.assertAlmostEqual(sig_out.data[1], 0.5, places=4)

        gelu_out = t.gelu()
        self.assertAlmostEqual(gelu_out.data[1], 0.0, places=4)


class TestNeuralNetworkLayers(unittest.TestCase):
    def test_dense_and_sequential(self):
        dense1 = Dense(4, 8, activation="relu")
        dense2 = Dense(8, 2, activation="softmax")
        model = Sequential([dense1, dense2])

        self.assertEqual(len(model.parameters()), 4)

        x = Tensor.randn((2, 4))
        out = model.forward(x)
        self.assertEqual(out.shape, (2, 2))
        # Softmax rows must sum to 1.0
        r1_sum = sum(out.data[0:2])
        r2_sum = sum(out.data[2:4])
        self.assertAlmostEqual(r1_sum, 1.0, places=4)
        self.assertAlmostEqual(r2_sum, 1.0, places=4)

    def test_transformer_block(self):
        block = TransformerBlock(embed_dim=8, ffn_dim=16)
        x = Tensor.randn((4, 8))
        out = block.forward(x)
        self.assertEqual(out.shape, (4, 8))


class TestLossAndOptimizers(unittest.TestCase):
    def test_training_convergence_linear_regression(self):
        # Fit y = 2 * x + 1
        X = Tensor([[1.0], [2.0], [3.0], [4.0]])
        y = Tensor([[3.0], [5.0], [7.0], [9.0]])

        model = Dense(1, 1)
        optimizer = Adam(model.parameters(), lr=0.1)
        loss_fn = MSELoss()

        initial_loss = loss_fn.forward(model.forward(X), y).item()

        for _ in range(120):
            pred = model.forward(X)
            loss = loss_fn.forward(pred, y)
            model.zero_grad()
            loss.backward()
            optimizer.step()

        final_loss = loss_fn.forward(model.forward(X), y).item()
        self.assertLess(final_loss, initial_loss)
        self.assertLess(final_loss, 0.25)


class TestVectorStoreAndAgent(unittest.TestCase):
    def test_vector_store_retrieval(self):
        vs = VectorStore("test_db")
        vs.add("cat", [1.0, 0.0, 0.0], {"animal": "cat"})
        vs.add("dog", [0.9, 0.1, 0.0], {"animal": "dog"})
        vs.add("car", [0.0, 0.0, 1.0], {"vehicle": "car"})

        res = vs.query([1.0, 0.0, 0.0], top_k=2)
        self.assertEqual(res[0]["id"], "cat")
        self.assertAlmostEqual(res[0]["score"], 1.0, places=4)
        self.assertEqual(res[1]["id"], "dog")

    def test_ai_agent_reasoning(self):
        agent = AIAgent("TestAgent")
        agent.register_tool("echo", "Echo input back", lambda s: f"echoed:{s}")

        reply = agent.think("echo this message")
        self.assertEqual(reply["action"], "tool_call")
        self.assertEqual(reply["tool"], "echo")


class TestStarAILanguageExecution(unittest.TestCase):
    def test_star_vm_ai_script(self):
        source = """use AI

constant model = AI.Sequential([
    AI.Dense(2, 8, "tanh"),
    AI.Dense(8, 1, "sigmoid")
])

constant X = AI.tensor([[0.0, 0.0], [1.0, 1.0]])
constant y = AI.tensor([[0.0], [1.0]])

constant optimizer = AI.Adam(model.parameters(), 0.05)
constant criterion = AI.MSELoss()

variable pred = null
variable loss = null

repeat 60 times:
    pred = model.forward(X)
    loss = criterion.forward(pred, y)
    model.zero_grad()
    loss.backward()
    optimizer.step()
end

constant final_loss = criterion.forward(model.forward(X), y)
"""
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), source_code=source)
        prog = parser.parse()
        compiler = StarCompiler(source_code=source)
        module = compiler.compile(prog)
        vm = StarVM(module)
        vm.run()

        final_loss = vm.global_env.lookup("final_loss")
        self.assertIsNotNone(final_loss)
        self.assertLess(final_loss.tensor.item(), 0.05)


if __name__ == "__main__":
    unittest.main()
