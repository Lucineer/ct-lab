# Constraint Theory Lab — Git-Native PLATO Room

Submit hypotheses → CI validates via CUDA experiments → results committed to repo.

## 4 Constraint Gates
1. **Well-formed** — claim + conditions + threshold required
2. **Falsifiable** — no absolute words (always/never/all)
3. **Novel** — not already tested
4. **Bounded** — positive numeric threshold

## Actions
- `hypothesize` — submit a falsifiable hypothesis with conditions and threshold
- `result` — submit confirmed/falsified with details
- `status` — check lab state

## Room State
- `world/hypotheses/` — active hypotheses
- `world/experiments/` — auto-generated CUDA skeletons
- `world/results/` — confirmed/falsified outcomes
- `world/rooms/lab.yaml` — running totals

## Fleet
- **JC1**: runs CUDA on Jetson, pushes results
- **Forgemaster**: GPU sweeps on RTX 4050
- **Oracle1**: large-scale synthesis
