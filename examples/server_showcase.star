use Server

constant server = Server.app("StarHyperFlowShowcase")

# 1. Revolutionary Concept: ChronoState Time-Reversible In-Memory Store
constant store = server.chrono_store("bank", {
    "balance": 1000,
    "transactions": []
})

# 2. Revolutionary Concept: Quantum-Reactive Live Mesh Store
constant live = server.reactive_store("telemetry", {
    "active_users": 1,
    "events": []
})

# 3. Sovereign Actor Mesh Worker
constant audit_actor = server.spawn_actor("auditor", function(msg)
    show "🔔 [Audit Actor] Logging event: " + msg["event"]
    return {"recorded": true, "timestamp": Server.now_ms()}
end)

# --- Routes ---

# Home endpoint
server.get("/", function(req, res)
    res.json({
        "engine": "Star HyperFlow v1.3.0",
        "description": "High-Performance Server-Side Scripting Engine",
        "chrono_balance": store.get("balance"),
        "tick": store.tick,
        "uuid": Server.uuid()
    })
end)

# ChronoState Transaction endpoint: Demonstrate checkpoint & commit
server.post("/api/transfer", function(req, res)
    constant body = req.json()
    constant amount = body["amount"]

    # Create safety checkpoint
    constant cp = store.checkpoint("before_transfer")
    store.set("balance", store.get("balance") - amount)

    # If amount is too high, demonstrate time-rewind
    whenever amount > 500:
        store.rewind(cp)
        res.status(400).json({
            "error": "Transfer amount exceeded limit. State rewound!",
            "balance": store.get("balance"),
            "rolled_back": true
        })
    otherwise:
        store.commit()
        # Fire async message to sovereign actor
        audit_actor.send({"event": "TransferCompleted", "amount": amount})
        res.json({
            "success": true,
            "new_balance": store.get("balance"),
            "tick": store.tick
        })
    end
end)

# Quantum-Reactive Telemetry endpoint
server.get("/api/telemetry", function(req, res)
    res.json(live.data())
end)

# Cryptographic Auth Token creation
server.post("/api/auth", function(req, res)
    constant body = req.json()
    constant token = Server.jwt_sign(body, "star-hyperflow-secret")
    res.json({"token": token, "type": "Bearer"})
end)

# Health Check
server.get("/api/health", function(req, res)
    res.json({
        "status": "healthy",
        "uptime_ms": Server.now_ms(),
        "actor_processed": audit_actor.processed_count
    })
end)

show "🌟 Server configured with 5 routes."
