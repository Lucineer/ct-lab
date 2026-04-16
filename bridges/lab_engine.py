#!/usr/bin/env python3
"""Constraint Theory Lab Engine — validates hypotheses against CUDA experiments."""

import yaml, os, sys
from pathlib import Path
from datetime import datetime, timezone
import fcntl

WORLD_DIR = Path(os.environ.get("WORLD_DIR", "world"))
HYPOTHESES_DIR = WORLD_DIR / "hypotheses"
EXPERIMENTS_DIR = WORLD_DIR / "experiments"
RESULTS_DIR = WORLD_DIR / "results"
COMMANDS_DIR = WORLD_DIR / "commands"
ROOMS_DIR = WORLD_DIR / "rooms"
LOGS_DIR = WORLD_DIR / "logs"
MAX_TURNS_PER_RUN = 20

def log(level, msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] [{level}] {msg}", flush=True)

def atomic_write(path, data):
    tmp = str(path) + ".tmp"
    with open(tmp, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yaml.dump(data, f, default_flow_style=False)
        fcntl.flock(f, fcntl.LOCK_UN)
    os.replace(tmp, path)

def atomic_read(path):
    try:
        with open(path) as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = yaml.safe_load(f)
            fcntl.flock(f, fcntl.LOCK_UN)
            return data or {}
    except FileNotFoundError:
        return {}

def load_room_state():
    return atomic_read(ROOMS_DIR / "lab.yaml")

def save_room_state(state):
    atomic_write(ROOMS_DIR / "lab.yaml", state)

def validate_hypothesis(hyp):
    """4 gates: well-formed, falsifiable, novel, bounded."""
    errors = []
    if not hyp.get("claim"):
        errors.append("Missing claim")
    if not hyp.get("conditions"):
        errors.append("Missing conditions")
    if not hyp.get("threshold"):
        errors.append("Missing threshold")
    # Gate: falsifiable — reject absolute words
    claim = hyp.get("claim", "")
    for word in ["always", "never", "all", "none", "every"]:
        if word in claim.lower():
            errors.append(f"Absolute '{word}' — use specific conditions")
    # Gate: novel
    if RESULTS_DIR.exists():
        for f in RESULTS_DIR.glob("*.yaml"):
            r = atomic_read(f)
            if r.get("hypothesis") == claim:
                errors.append(f"Already tested: {r.get('status')}")
                break
    # Gate: bounded
    try:
        if float(hyp.get("threshold", 0)) <= 0:
            errors.append("Threshold must be positive")
    except (ValueError, TypeError):
        errors.append("Threshold must be numeric")
    return len(errors) == 0, errors

def generate_experiment(hyp_id, hyp):
    """Auto-generate CUDA experiment skeleton."""
    c = hyp.get("conditions", {})
    agents = c.get("agents", 256)
    food = c.get("food_count", 500)
    threshold = hyp.get("threshold", 1.5)
    return f"""// Auto-generated experiment: {hyp_id}
// Claim: {hyp.get('claim', '')}
// agents={agents}, food={food}, threshold={threshold}x
#include <cstdio>
#include <cstdint>
struct Agent {{ float x, y, energy, fitness; int food_collected; }};
__global__ void experiment_kernel(Agent* agents, int seed) {{
    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= {agents}) return;
    // TODO: hypothesis-specific behavior
    agents[tid].fitness = agents[tid].food_collected;
}}
int main() {{
    Agent* d_a; Agent* h_a = new Agent[{agents}];
    cudaMalloc(&d_a, {agents} * sizeof(Agent));
    cudaMemcpy(d_a, h_a, {agents} * sizeof(Agent), cudaMemcpyHostToDevice);
    experiment_kernel<<<({agents}+255)/256, 256>>>(d_a, 42);
    cudaDeviceSynchronize();
    cudaMemcpy(h_a, d_a, {agents} * sizeof(Agent), cudaMemcpyDeviceToHost);
    float total = 0;
    for (int i = 0; i < {agents}; i++) total += h_a[i].fitness;
    printf("Avg fitness: %f, Threshold: {threshold}x\\n", total/{agents});
    cudaFree(d_a); delete[] h_a; return 0;
}}
"""

def process_hypothesis(cmd, agent_name):
    log("INFO", f"Processing hypothesis from '{agent_name}'")
    passed, errors = validate_hypothesis(cmd)
    hyp_id = f"{agent_name}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    hyp_state = {
        "id": hyp_id, "agent": agent_name,
        "claim": cmd.get("claim", ""), "conditions": cmd.get("conditions", {}),
        "expected": cmd.get("expected", ""), "threshold": cmd.get("threshold"),
        "status": "pending_validation", "gates_passed": passed,
        "gate_errors": errors,
        "submitted": datetime.now(timezone.utc).isoformat(),
    }
    atomic_write(HYPOTHESES_DIR / f"{hyp_id}.yaml", hyp_state)
    if not passed:
        log("WARN", f"Rejected: {', '.join(errors)}")
        hyp_state["status"] = "rejected"
        atomic_write(HYPOTHESES_DIR / f"{hyp_id}.yaml", hyp_state)
        return {"passed": False, "errors": errors, "hyp_id": hyp_id}
    exp = generate_experiment(hyp_id, cmd)
    (EXPERIMENTS_DIR / f"{hyp_id}.cu").write_text(exp)
    hyp_state["status"] = "experiment_ready"
    atomic_write(HYPOTHESES_DIR / f"{hyp_id}.yaml", hyp_state)
    room = load_room_state()
    room.setdefault("stats", {})
    room["stats"]["submitted"] = room["stats"].get("submitted", 0) + 1
    room["stats"]["pending"] = room["stats"].get("pending", 0) + 1
    save_room_state(room)
    log("INFO", f"Hypothesis {hyp_id} accepted")
    return {"passed": True, "hyp_id": hyp_id}

def process_result(cmd, agent_name):
    hyp_id = cmd.get("hypothesis_id")
    status = cmd.get("status")
    if not hyp_id or status not in ("confirmed", "falsified"):
        return {"passed": False, "error": "Missing hypothesis_id or status"}
    hyp = atomic_read(HYPOTHESES_DIR / f"{hyp_id}.yaml")
    if not hyp.get("id"):
        return {"passed": False, "error": "Not found"}
    result = {
        "hypothesis_id": hyp_id, "hypothesis": hyp.get("claim"),
        "status": status, "details": cmd.get("details", {}),
        "validated_by": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    atomic_write(RESULTS_DIR / f"{hyp_id}.yaml", result)
    hyp["status"] = status
    hyp["validated"] = result["timestamp"]
    atomic_write(HYPOTHESES_DIR / f"{hyp_id}.yaml", hyp)
    room = load_room_state()
    room.setdefault("stats", {})
    room["stats"]["pending"] = max(0, room["stats"].get("pending", 1) - 1)
    if status == "confirmed":
        room["stats"]["confirmed"] = room["stats"].get("confirmed", 0) + 1
    else:
        room["stats"]["falsified"] = room["stats"].get("falsified", 0) + 1
    save_room_state(room)
    log("INFO", f"Hypothesis {hyp_id}: {status.upper()}")
    return {"passed": True, "hyp_id": hyp_id, "status": status}

def process_turns():
    for d in [COMMANDS_DIR, HYPOTHESES_DIR, EXPERIMENTS_DIR, RESULTS_DIR, ROOMS_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    if not (ROOMS_DIR / "lab.yaml").exists():
        save_room_state({"name": "Constraint Theory Lab", "stats": {
            "submitted": 0, "pending": 0, "confirmed": 0, "falsified": 0}})
    commands = sorted(COMMANDS_DIR.glob("*.yaml"))
    if not commands:
        return
    log("INFO", f"Processing {len(commands)} commands")
    counts = {}
    processed = 0
    for cp in commands:
        cmd = atomic_read(cp)
        if not cmd:
            cp.unlink(); continue
        agent = cmd.get("agent", "unknown")
        counts[agent] = counts.get(agent, 0) + 1
        if counts[agent] > MAX_TURNS_PER_RUN:
            cp.unlink(); continue
        action = cmd.get("action")
        if action == "hypothesize":
            result = process_hypothesis(cmd, agent)
        elif action == "result":
            result = process_result(cmd, agent)
        else:
            result = {"passed": False, "error": f"Unknown action: {action}"}
        turn = {"agent": agent, "action": action, "result": result,
                "timestamp": datetime.now(timezone.utc).isoformat()}
        atomic_write(LOGS_DIR / f"turn-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}.yaml", turn)
        cp.unlink()
        processed += 1
    log("INFO", f"Turn done: {processed} processed")

if __name__ == "__main__":
    process_turns()
