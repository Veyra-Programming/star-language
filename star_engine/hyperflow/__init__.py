"""
Star HyperFlow Engine — High-Performance Server & Reactive Concurrency Subsystem
Authoritative Reference: STAR_SERVER_SPEC.md

Exports:
- ServerApp, StarServerApp
- Request, StarRequestObj
- Response, StarResponseObj
- ChronoStore, StarChronoStore
- ReactiveStore, StarReactiveStore
- ActorMesh, StarActorRef
- HyperRouter, RouteMatch
- run_benchmark
"""

from star_engine.hyperflow.router import HyperRouter, RouteMatch
from star_engine.hyperflow.chrono import ChronoStore, StarChronoStore
from star_engine.hyperflow.reactive_mesh import ReactiveStore, StarReactiveStore
from star_engine.hyperflow.actor import ActorMesh, StarActorRef
from star_engine.hyperflow.server import (
    ServerApp, StarServerApp, Request, StarRequestObj, Response, StarResponseObj
)
from star_engine.hyperflow.benchmark import run_benchmark

__version__ = "1.3.0"
__all__ = [
    "ServerApp", "StarServerApp",
    "Request", "StarRequestObj",
    "Response", "StarResponseObj",
    "ChronoStore", "StarChronoStore",
    "ReactiveStore", "StarReactiveStore",
    "ActorMesh", "StarActorRef",
    "HyperRouter", "RouteMatch",
    "run_benchmark",
]
