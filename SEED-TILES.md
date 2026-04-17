# CT Lab — PLATO Room for Constraint Theory Validation

A git-native PLATO room where hypotheses are submitted, validated via CUDA, and accumulated as tiles.

## Cross-Pollination

This room cross-pollinates with:
- **Lucineer/plato** — The reference PLATO system (tiles format)
- **Lucineer/flux-emergence-research** — Raw CUDA experiments (39+ laws)
- **Lucineer/constraint-theory-papers** — Mathematical foundation (5 papers)

## Seed Tiles

The room ships with tiles covering the 39 confirmed laws from 80+ CUDA experiments.

### Top Laws (confirmed)

- **Law 1: Grab range dominates** — 2.40x fitness from grab range alone. No other single mechanism comes close.
- **Law 2: Cooperation + clustering** — 2.19x when agents cooperate AND cluster. Separately they're weaker.
- **Law 3: Seasonal availability** — 9.2x with feast/famine cycles. The single largest effect in the entire research program.
- **Law 4: Stacked mechanisms** — 5.71x when multiple confirmed mechanisms are combined. The fleet rule.
- **Law 5: DCS ring buffer K=1** — +38% over no DCS. Single most-recent food location shared.
- **Law 6: DCS inverse to perception** — Small grab range (4-8): +72-99% DCS lift. Large range (24-32): +10-20%.
- **Law 7: DCS is local** — Dense 64x64: +90%. Sparse 512x512: -42%. DCS needs density.
- **Law 8: Speed inverted-U with DCS** — Peak +221% at speed 3. Fast agents overshoot targets.
- **Law 9: Herding is pure overhead** — Even in abundance: -10%. Scarcity: -48%. Never herd.
- **Law 10: Instinct is safety override, not brain** — ROLE beats INSTINCT 2.23x. Instinct for emergencies only.
- **Law 11: DCS ring buffer harmful with moving food** — Speed=0: +23%. Speed>=1: -6% to -22%.
- **Law 12: Individual perception dominates DCS for mobile targets** — No sharing strategy beats individual perception when food moves.
- **Law 13: Perception cost cliff at ~0.03** — Optimal at 0.001 (+8.5% over free). Small cost filters unnecessary scans.
- **Law 14: Single guild maximizes DCS** — 1 guild +25% > 8 guilds +18% > 16 guilds neutral.
- **Law 15: Cultural inheritance matters only at high mortality** — +32% at high death. Converge-to-best > memory.
- **Law 16: DCS critical at extreme scarcity × large perception** — The practical sweet spot.
- **Law 17: Multi-point DCS fixes stampede** — TOP-8 distributed knowledge +19% over no DCS.
- **Law 18: Larger swarms increase per-agent fitness** — Fleet effect. More agents find food faster for everyone.
- **Law 19: DCS benefit inversely proportional to perception range** — The small-grab-range agent benefits most from shared knowledge.
- **Law 20: DCS lift independent of population** — ~2.5x constant from 128 to 2048 agents.

### Falsified Mechanisms (DO NOT USE)

These were tested and proven wrong:
- Energy sharing
- Trading
- Pheromones
- Hierarchy
- Signaling
- Evolution
- Lifecycle
- Memory (unconditional)
- Reciprocity
- Voting
- Environmental gradients
- Multi-species
- Cognitive maps
- Adaptive detection
- Speed asymmetry
- Anti-convergence
- Temporal coordination
- Multi-objective (uniform)
- Niche construction
- Gossip
- Trails
- Herding
- Instinct-as-brain
- DCS-with-migration
- Fragmented-guilds

### Fleet Rules

1. Pre-assign roles
2. Maximize grab range
3. Design for scarcity
4. Cluster at spawn
5. Stack confirmed mechanisms
6. Use prediction ONLY when environment is predictable
7. NEVER herd or share unstructured information
8. Use instinct only as survival override
9. Single guild for DCS
10. DCS only for static resources
11. DCS optimal at K=1-2
12. DCS is local (needs density)
13. Moderate movement speed for DCS

## How to Use This Room

### Submit a Hypothesis
```yaml
# world/hypotheses/my-hypothesis.yaml
hypothesis_id: ct-40
claim: "Perception range has diminishing returns above 16 cells"
conditions:
  - agents: 256
  - food: 200
  - world_size: 128
threshold: "fitness_improvement < 5% when doubling range from 16 to 32"
status: pending
```

### Record a Result
```yaml
# world/results/ct-40.yaml
hypothesis_id: ct-40
outcome: confirmed
details: "Doubling perception from 16 to 32 improved fitness by only 3.2% (p<0.01)"
experiment: experiment-perception-doubling.cu
date: 2026-04-16
```

### Convert to Tile
Every confirmed/falsified result becomes a PLATO tile:
```json
{
  "instruction": "Does perception range have diminishing returns above 16?",
  "input": "256 agents, 200 food, 128x128 world",
  "output": "Yes. Doubling from 16 to 32 improved fitness only 3.2%. Confirmed in experiment-perception-doubling.cu",
  "metadata": {"room_id": "ct_lab", "source": "jc1", "hypothesis_id": "ct-40"}
}
```

## Bridge to PLATO Portable

```bash
# Export CT Lab tiles to portable PLATO
python3 scripts/export_tiles.py --room ct_lab --format instruction-input-output

# Import into PLATO portable
cp ct_lab_tiles.json /path/to/plato/data/tiles/ct_lab.json
```
