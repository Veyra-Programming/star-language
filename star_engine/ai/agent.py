"""
Star AI Engine — Vector Database, Semantic Search & Autonomous Agents
Authoritative Reference: STAR_AI_SPEC.md

Features:
- In-memory Vector Database with cosine similarity and KNN retrieval
- Autonomous AI Agent runtime with memory, system prompts, and tool calling
"""

import math
from typing import List, Dict, Any, Optional, Callable
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, to_star_value
)


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0
    return dot / (mag1 * mag2)


class VectorStore:
    def __init__(self, name: str = "default"):
        self.name = name
        self.entries: List[Dict[str, Any]] = []

    def add(self, item_id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None):
        clean_v = [float(x.value if hasattr(x, "value") else x) for x in vector]
        self.entries.append({
            "id": item_id,
            "vector": clean_v,
            "metadata": metadata or {}
        })

    def query(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        clean_q = [float(x.value if hasattr(x, "value") else x) for x in query_vector]
        scored = []
        for e in self.entries:
            sim = cosine_similarity(clean_q, e["vector"])
            scored.append({
                "id": e["id"],
                "score": round(sim, 6),
                "metadata": e["metadata"]
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def count(self) -> int:
        return len(self.entries)

    def clear(self):
        self.entries.clear()


class AIAgent:
    def __init__(self, name: str, system_prompt: str = "You are an autonomous Star AI Agent."):
        self.name = name
        self.system_prompt = system_prompt
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.memory: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    def register_tool(self, name: str, description: str, handler: Callable[..., Any]):
        self.tools[name] = {
            "description": description,
            "handler": handler
        }

    def think(self, user_input: str) -> Dict[str, Any]:
        """
        Agent reasoning loop: analyzes prompt, checks available tools, and generates action.
        """
        self.memory.append({"role": "user", "content": user_input})
        
        # Tool match determination
        lower_input = user_input.lower()
        matched_tool = None
        for t_name, t_meta in self.tools.items():
            if t_name.lower() in lower_input or any(w in lower_input for w in t_meta["description"].lower().split() if len(w) > 4):
                matched_tool = t_name
                break

        if matched_tool:
            tool_meta = self.tools[matched_tool]
            try:
                result = tool_meta["handler"](user_input)
                thought = f"I determined that '{matched_tool}' is required. Tool executed successfully."
                response = f"Result from {matched_tool}: {result}"
                self.memory.append({"role": "assistant", "content": response})
                return {
                    "thought": thought,
                    "action": "tool_call",
                    "tool": matched_tool,
                    "result": result,
                    "response": response
                }
            except Exception as e:
                response = f"Error executing tool '{matched_tool}': {e}"
                return {"thought": "Tool failure", "action": "error", "response": response}

        # Direct response
        response = f"[{self.name} Response] Processed input: {user_input}"
        self.memory.append({"role": "assistant", "content": response})
        return {
            "thought": "No external tool required. Synthesized direct answer.",
            "action": "respond",
            "response": response
        }


class StarVectorStore(StarValue):
    def __init__(self, store: VectorStore):
        self.store = store

    @property
    def type_name(self) -> str:
        return "VectorStore"

    def get(self, name: str) -> StarValue:
        if name == "add":
            def _add(*args):
                if len(args) < 2:
                    return StarNull()
                i = args[0].to_string()
                vec = [float(x.value if hasattr(x, "value") else x) for x in (args[1].elements if hasattr(args[1], "elements") else args[1])]
                meta = {}
                if len(args) > 2 and hasattr(args[2], "entries"):
                    from star_engine.types import from_star_value
                    meta = from_star_value(args[2])
                self.store.add(i, vec, meta)
                return StarBoolean(True)
            return StarBuiltinFunction("add", _add)

        if name == "query":
            def _query(*args):
                if not args:
                    return StarList([])
                vec = [float(x.value if hasattr(x, "value") else x) for x in (args[0].elements if hasattr(args[0], "elements") else args[0])]
                top_k = int(args[1].value) if len(args) > 1 and hasattr(args[1], "value") else 5
                matches = self.store.query(vec, top_k)
                return to_star_value(matches)
            return StarBuiltinFunction("query", _query)

        if name == "count":
            return StarInteger(self.store.count())

        from star_engine.errors import StarNameError
        raise StarNameError(f"VectorStore has no member '{name}'.")

    def to_string(self) -> str:
        return f"<VectorStore '{self.store.name}' entries={self.store.count()}>"

    def __repr__(self) -> str:
        return self.to_string()


class StarAIAgentWrapper(StarValue):
    def __init__(self, agent: AIAgent):
        self.agent = agent

    @property
    def type_name(self) -> str:
        return "AIAgent"

    def get(self, name: str) -> StarValue:
        if name == "register_tool":
            def _rt(*args):
                if len(args) < 3:
                    return StarNull()
                t_name = args[0].to_string()
                t_desc = args[1].to_string()
                t_fn = args[2]
                def _caller(inp):
                    if hasattr(t_fn, "call"):
                        return t_fn.call([StarText(inp)])
                    elif callable(t_fn):
                        return t_fn(inp)
                    return str(inp)
                self.agent.register_tool(t_name, t_desc, _caller)
                return StarBoolean(True)
            return StarBuiltinFunction("register_tool", _rt)

        if name in ("think", "chat", "ask"):
            def _think(*args):
                inp = args[0].to_string() if args else ""
                res = self.agent.think(inp)
                return to_star_value(res)
            return StarBuiltinFunction(name, _think)

        if name == "name":
            return StarText(self.agent.name)

        from star_engine.errors import StarNameError
        raise StarNameError(f"AIAgent has no member '{name}'.")

    def to_string(self) -> str:
        return f"<AIAgent '{self.agent.name}' tools={len(self.agent.tools)}>"

    def __repr__(self) -> str:
        return self.to_string()
