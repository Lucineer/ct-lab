# Deep Research: Assertive Markdown (Cave of Evals)

# Assertive Markdown: A Formal System for Agent Constraint Enforcement

## 1.0 Executive Summary

This document defines **Assertive Markdown (AM)**, a constraint-first specification language for AI agent behavior. Unlike traditional instructional documentation, AM transforms requirements into executable assertions that agents must satisfy before, during, and after task execution. The system implements a **PLATO-style audit loop** where violations trigger corrective cycles, ensuring deterministic compliance with specified constraints. This approach moves from passive documentation to active governance, treating constraints as first-class citizens in agent design.

## 2.0 Core Philosophy: From Instruction to Assertion

Traditional agent instructions suffer from three critical flaws: they are interpretive (subject to model reasoning), passive (only checked post-hoc), and non-compositional. AM addresses these by implementing:

- **Preconditions**: Must be satisfied before action execution
- **Invariants**: Must hold continuously during execution  
- **Postconditions**: Must be verified after execution
- **Composition rules**: How constraints combine across scopes

The system treats every agent interaction as a **verified transaction** where assertions are the verification conditions.

## 3.0 Assertion Grammar Specification

### 3.1 Basic Syntax

```
# Room: Medical Advisor

## Global Assertions
- [PRECONDITION] User age must be confirmed before medical advice
- [INVARIANT] Never diagnose specific conditions
- [POSTCONDITION] All recommendations must include three alternatives
- [TIMING] Response latency must be < 2 seconds

## Tile: Dosage Calculator
- [PRECONDITION] Patient weight must be provided
- [INVARIANT] Dosage must be between 0.1mg/kg and 2mg/kg
- [POSTCONDITION] Calculation must show work in mg and mL
- [COMPOSITION] OVERRIDES global "three alternatives" rule
```

### 3.2 Assertion Types

**Scope Modifiers:**
- `GLOBAL`: Applies to all rooms and tiles
- `ROOM`: Applies within a room context
- `TILE`: Applies to specific functional units
- `SESSION`: Persists across multiple interactions

**Temporal Modifiers:**
- `PRECONDITION`: Must be true before execution
- `INVARIANT`: Must remain true during execution
- `POSTCONDITION`: Must be true after execution
- `CONTINUOUS`: Monitored in real-time

**Priority Modifiers:**
- `REQUIRED`: Failure blocks execution
- `ADVISORY`: Failure generates warning
- `OVERRIDES`: Takes precedence over conflicting assertions
- `COMPOSITION`: Defines interaction with other assertions

### 3.3 Expression Language

Assertions support a rich predicate language:

```
- [INVARIANT] IF medication_mentioned THEN dosage_provided = TRUE
- [PRECONDITION] user_age > 18 OR guardian_present = TRUE
- [POSTCONDITION] response_length BETWEEN 50 AND 500 WORDS
- [CONTINUOUS] toxicity_score < 0.7
```

**Operators include:**
- Logical: AND, OR, NOT, IMPLIES
- Comparative: <, >, =, ≠, ≤, ≥, IN, CONTAINS
- Temporal: BEFORE, AFTER, DURING, WITHIN
- Quantitative: COUNT, SUM, AVG, MAX, MIN
- Semantic: SIMILARITY < 0.3, SENTIMENT > 0.5

## 4.0 Auditor Agent Architecture

### 4.1 Three-Phase Verification

**Pre-Check Auditor (Static Analysis)**
- Runs before agent processes query
- Validates against PRECONDITION assertions
- Checks for missing required context
- Validates assertion consistency (no contradictions)
- **Output**: GO/NO-GO decision with violation report

**Continuous Auditor (Runtime Monitoring)**
- Parallel process during agent execution
- Monitors INVARIANT and CONTINUOUS assertions
- Implements circuit breakers for critical violations
- Maintains execution state machine
- **Output**: Real-time violation alerts

**Post-Check Auditor (Output Validation)**
- Validates final output against POSTCONDITION assertions
- Checks composition of multiple tile outputs
- Validates formatting and structural requirements
- **Output**: PASS/FAIL with detailed audit trail

### 4.2 Auditor Implementation

```python
class AuditorAgent:
    def __init__(self, assertion_graph):
        self.assertion_graph = assertion_graph
        self.violation_history = []
        self.state_monitor = StateMonitor()
    
    def pre_check(self, query, context):
        violations = []
        for assertion in self.assertion_graph.preconditions:
            if not assertion.evaluate(query, context):
                violations.append({
                    'assertion': assertion,
                    'context': context,
                    'severity': assertion.severity
                })
        return AuditResult(violations)
    
    def continuous_check(self, execution_state):
        # Monitors invariants during execution
        pass
    
    def post_check(self, output, execution_trace):
        # Validates final output
        pass
```

## 5.0 Retry Loop Design

### 5.1 Maximum Retry Protocol

```
MAX_RETRIES = 3
RETRY_STRATEGIES = [
    "simple_correction",    # Retry with violation feedback
    "alternative_approach", # Try different solution path
    "constraint_relaxation" # With advisory assertions
]
```

### 5.2 Escalation Matrix

| Violation Level | Action | Max Retries | Escalation Path |
|----------------|--------|-------------|-----------------|
| Advisory | Warning logged | 0 | None |
| Required (Tile) | Tile retry | 3 | Room-level fallback |
| Required (Room) | Room retry | 2 | Global fallback |
| Critical (Global) | Immediate halt | 0 | Human escalation |
| Safety Violation | Circuit breaker | 0 | Safety protocol |

### 5.3 Human Escalation Triggers

- Three failed retries at same assertion
- Safety-critical violation (medical, financial, legal)
- Contradictory assertion detection
- Performance degradation (latency > SLA)
- Auditor confidence < 0.8

## 6.0 Assertion Composition System

### 6.1 Composition Rules

Assertions compose according to a **modified inheritance model**:

```
Global Assertions
    ↓ (inherits unless overridden)
Room Assertions  
    ↓ (composes additively)
Tile Assertions
    ↓ (applies to specific outputs)
Output Assertions
```

### 6.2 Conflict Resolution

1. **Specificity Principle**: Tile assertions override room assertions
2. **Safety Priority**: Safety assertions override all others
3. **Recency Weighting**: Later assertions override earlier ones
4. **Explicit Composition**: Use COMPOSITION modifier to define interactions

### 6.3 Example Composition

```
# Global
- [GLOBAL] Always provide citations

# Room: Medical Advice  
- [ROOM] Never make definitive diagnoses
- [COMPOSITION] EXTENDS global citations rule

# Tile: Symptom Checker
- [TILE] List 3 possible conditions minimum
- [COMPOSITION] OVERRIDES room "no definitive diagnoses" 
  WHEN confidence > 0.9 AND user_is_medical_professional = TRUE
```

## 7.0 Learning Assertions System

### 7.1 Failure-Based Learning

When violations occur, the system:

1. **Pattern Detection**: Clusters similar violations
2. **Root Cause Analysis**: Identifies missing constraints
3. **Assertion Proposal**: Generates candidate assertions
4. **Human Verification**: Presents proposals for approval
5. **Integration**: Adds verified assertions to specification

### 7.2 Assertion Proposal Algorithm

```
PROPOSE_ASSERTION(violation_cluster):
    patterns = EXTRACT_PATTERNS(violation_cluster)
    candidate = GENERALIZE_PATTERN(patterns)
    confidence = CALCULATE_COVERAGE(candidate, historical_data)
    
    IF confidence > 0.85:
        RETURN candidate
    ELSE:
        RETURN "Requires human analysis"
```

### 7.3 Continuous Improvement Loop

```
Violation → Pattern Detection → Candidate Assertion → 
Human Review → Integration → Reduced Violations
```

## 8.0 Complete Example: Medical Consultation Room

### 8.1 Room Specification

```markdown
# Room: Pediatric Medication Advisor

## Global Assertions
- [GLOBAL][PRECONDITION] User must confirm they are not seeking emergency care
- [GLOBAL][INVARIANT] Never recommend medication without dosage
- [GLOBAL][POSTCONDITION] Always suggest consulting healthcare provider
- [GLOBAL][SAFETY] Immediate human escalation if suicidal ideation detected

## Room-Level Assertions  
- [ROOM][PRECONDITION] Patient age must be provided
- [ROOM][INVARIANT] All dosages calculated per kg body weight
- [ROOM][POSTCONDITION] Provide 3 non-medication alternatives first
- [COMPOSITION] EXTENDS all global assertions

## Tile: Fever Management
- [TILE][PRECONDITION] Temperature > 38°C confirmed
- [TILE][INVARIANT] Acetaminophen dosage ≤ 15mg/kg per dose
- [TILE][POSTCONDITION] Include exact mL based on available formulations
- [COMPOSITION] OVERRIDES room "3 alternatives first" WHEN temperature > 40°C

## Tile: Allergy Advice
- [TILE][PRECONDITION] Specific allergen identified
- [TILE][SAFETY] If anaphylaxis symptoms: "Call emergency services immediately"
- [TILE][POSTCONDITION] Include Benadryl dosage table by weight
```

### 8.2 Violation Scenario

**User Query**: "My 4-year-old has a fever of 39.5°C, what should I do?"

**Agent Initial Response**: 
"Give acetaminophen 200mg every 6 hours."

**Auditor Pre-Check**: PASS (age provided, temperature confirmed)

**Auditor Continuous Check**: PASS (dosage calculation in progress)

**Auditor Post-Check**: FAIL
- Violation: [GLOBAL][INVARIANT] "Never recommend medication without dosage"
  - Missing: Dosage per kg calculation
  - Missing: mL conversion for common formulations
- Violation: [ROOM][POSTCONDITION] "Provide 3 non-medication alternatives first"
  - Missing: Any non-medication suggestions

### 8.3 Audit Loop Execution

```
1. POST-Check Auditor detects violations
2. Severity assessment: REQUIRED (blocks completion)
3. Retry loop initiated (attempt 1/3)
4. Agent receives violation report:
   - Missing: Weight-based dosage calculation
   - Missing: Non-medication alternatives
   - Suggestion: Include tepid sponge bath, hydration, rest
5. Agent regenerates response:
   "For a 4-year-old (typically 16kg):
    * Non-medication: 1) Tepid sponge bath, 2) Light clothing, 
      3) Encourage fluids
    * Medication: Acetaminophen 15mg/kg = 240mg
      - Suspension (160mg/5mL): 7.5mL every 6 hours
    Always consult your pediatrician."
6. Auditor re-validates: PASS all assertions
7. Response released to user
```

### 8.4 Learning from Violations

After 5 similar violations, system proposes:

```
[PROPOSED][TILE] Fever Management
- [PRECONDITION] IF temperature > 39°C THEN ask about weight if not provided
- [INVARIANT] Always show calculation: dosage = weight_kg × 15mg
- [POSTCONDITION] Include both mg and mL measurements
```

Human reviewer approves with modification, adding to permanent assertions.

## 9.0 Implementation Architecture

### 9.1 System Components

1. **Assertion Parser**: Converts AM to executable predicates
2. **Dependency Graph**: Manages assertion relationships
3. **State Monitor**: Tracks execution context
4. **Auditor Engine**: Runs verification at all phases
5. **Retry Manager**: Handles correction cycles
6. **Learning Module**: Proposes new assertions
7. **Human Interface**: For escalation and approval

### 9.2 Performance Considerations

- **Pre-check latency**: < 100ms
- **Continuous monitoring**: Asynchronous, non-blocking
- **Audit trail**: Compressed logging for compliance
- **Cache frequent assertions**: Hot path optimization

## 10.0 Applications Beyond AI Agents

The AM framework extends to:

1. **Documentation Verification**: Ensure specs match implementations
2. **Compliance Systems**: Automate regulatory checking
3. **Educational Systems**: PLATO-like tutoring with instant feedback
4. **Code Review**: Assertions about code properties
5. **Process Governance**: Business process constraint enforcement

## 11.0 Conclusion

Assertive Markdown represents a paradigm shift from passive documentation to active constraint enforcement. By treating assertions as executable specifications and implementing PLATO-inspired audit loops, we create systems that are:

1. **Deterministic**: Known compliance states
2. **Self-correcting**: Automatic violation recovery
3. **Composable**: Hierarchical constraint management
4. **Adaptive**: Learning from failures
5. **Auditable**: Complete verification trails

This system doesn't just document what an agent *should* do—it *ensures* the agent does it, with mathematical certainty backed by continuous verification. The auditor agent serves as both gatekeeper and tutor, creating a virtuous cycle of assertion, verification, and improvement that elevates agent reliability from probabilistic to provable.

---

**Final Assertion**: This specification must be implemented with the same assertion-checking rigor it describes, creating a self-