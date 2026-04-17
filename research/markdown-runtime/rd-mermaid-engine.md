# R&D: Mermaid-to-Action Engine — DeepSeek-chat

# Mermaid State Diagram Parser with Transition Table

## Complete Parser Implementation

```python
import re
from typing import Dict, List, Optional, Tuple

class MermaidStateDiagramParser:
    """Parser for Mermaid stateDiagram-v2 subset to transition table."""
    
    def __init__(self):
        self.transitions = {}
        self.initial_state = None
        self.final_state = None
        self.states = set()
        
    def parse(self, mermaid_text: str) -> Dict:
        """
        Parse Mermaid state diagram text into transition table.
        
        Args:
            mermaid_text: String containing Mermaid state diagram
            
        Returns:
            Dictionary with initial, final states and transitions
        """
        # Reset state
        self.transitions = {}
        self.initial_state = None
        self.final_state = None
        self.states = set()
        
        # Process each line
        lines = mermaid_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('%%'):
                continue
            
            # Skip the diagram declaration
            if line.startswith('stateDiagram-v2'):
                continue
            
            # Parse state transitions
            self._parse_transition_line(line)
        
        # Build result
        return {
            'initial': self.initial_state,
            'final': self.final_state,
            'transitions': self._normalize_transitions(),
            'states': list(self.states)
        }
    
    def _parse_transition_line(self, line: str):
        """Parse a single transition line."""
        # Remove inline comments
        line = line.split('%%')[0].strip()
        
        # Pattern for transitions: State1 --> State2 : label
        # Also handles [*] as initial/final states
        pattern = r'^\s*(?P<from_state>\[?\w+\]?)\s*-->\s*(?P<to_state>\[?\w+\]?)(?:\s*:\s*(?P<label>.+))?$'
        
        match = re.match(pattern, line)
        if not match:
            return
        
        from_state = match.group('from_state').strip()
        to_state = match.group('to_state').strip()
        label = match.group('label')
        
        # Handle initial state ([*])
        if from_state == '[*]':
            self.initial_state = to_state
            self.states.add(to_state)
            return
        
        # Handle final state ([*])
        if to_state == '[*]':
            self.final_state = from_state
            self.states.add(from_state)
            return
        
        # Normalize state names (remove brackets if present)
        from_state = self._normalize_state_name(from_state)
        to_state = self._normalize_state_name(to_state)
        
        # Add to states set
        self.states.add(from_state)
        self.states.add(to_state)
        
        # Create normalized label
        if label:
            # Convert label to snake_case for use as key
            normalized_label = self._normalize_label(label.strip())
        else:
            normalized_label = 'transition'
        
        # Add to transitions dictionary
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        
        # Handle multiple transitions with same label by appending number
        base_label = normalized_label
        counter = 1
        while normalized_label in self.transitions[from_state]:
            normalized_label = f"{base_label}_{counter}"
            counter += 1
        
        self.transitions[from_state][normalized_label] = to_state
    
    def _normalize_state_name(self, state_name: str) -> str:
        """Normalize state names by removing brackets."""
        if state_name.startswith('[') and state_name.endswith(']'):
            return state_name[1:-1]
        return state_name
    
    def _normalize_label(self, label: str) -> str:
        """Convert label to snake_case identifier."""
        # Convert to lowercase
        label = label.lower()
        # Replace spaces and special characters with underscores
        label = re.sub(r'[^\w\s]', '_', label)
        label = re.sub(r'\s+', '_', label)
        # Remove consecutive underscores
        label = re.sub(r'_+', '_', label)
        # Remove leading/trailing underscores
        label = label.strip('_')
        return label
    
    def _normalize_transitions(self) -> Dict:
        """Ensure all states are present in transitions dict."""
        normalized = {}
        for state in self.states:
            normalized[state] = self.transitions.get(state, {})
        return normalized
    
    def validate_state_machine(self, transition_table: Dict) -> List[str]:
        """Validate the parsed state machine for consistency."""
        warnings = []
        
        # Check for unreachable states
        reachable = set()
        if transition_table['initial']:
            reachable.add(transition_table['initial'])
        
        # Find all reachable states
        for from_state, transitions in transition_table['transitions'].items():
            if from_state in reachable:
                for to_state in transitions.values():
                    reachable.add(to_state)
        
        # Check for states that aren't reachable
        all_states = set(transition_table['states'])
        unreachable = all_states - reachable
        if unreachable:
            warnings.append(f"Unreachable states: {', '.join(unreachable)}")
        
        # Check for states with no outgoing transitions (except final)
        for state in all_states:
            if (state != transition_table['final'] and 
                not transition_table['transitions'].get(state)):
                warnings.append(f"State '{state}' has no outgoing transitions")
        
        return warnings


# Example usage and testing
def test_parser():
    """Test the parser with the provided example."""
    
    mermaid_example = """stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: query received
    Processing --> TileMatch: tiles found
    Processing --> LLMSynth: no tiles
    TileMatch --> Respond: tile selected
    LLMSynth --> Respond: synthesis done
    Respond --> [*]
    
    %% This is a comment
    """
    
    parser = MermaidStateDiagramParser()
    result = parser.parse(mermaid_example)
    
    print("Parsed Transition Table:")
    print(json.dumps(result, indent=2))
    
    # Validate
    warnings = parser.validate_state_machine(result)
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    return result


if __name__ == "__main__":
    import json
    test_parser()
```

## Integration with PLATO Room for Agent State Management

### 1. State Machine Manager Class

```python
class AgentStateManager:
    """
    Manages agent state transitions based on keyword triggers.
    Integrates with PLATO room for agent coordination.
    """
    
    def __init__(self, mermaid_diagram: str):
        self.parser = MermaidStateDiagramParser()
        self.transition_table = self.parser.parse(mermaid_diagram)
        self.current_state = self.transition_table['initial']
        self.state_history = []
        self.keyword_triggers = {}
        self._build_keyword_mappings()
    
    def _build_keyword_mappings(self):
        """Build keyword to transition mapping from parsed diagram."""
        for from_state, transitions in self.transition_table['transitions'].items():
            for trigger, to_state in transitions.items():
                # Store both the normalized trigger and variations
                self.keyword_triggers[trigger] = {
                    'from_state': from_state,
                    'to_state': to_state,
                    'keywords': [trigger.replace('_', ' ')]
                }
    
    def add_keyword_variants(self, trigger: str, variants: List[str]):
        """Add alternative keywords for a trigger."""
        if trigger in self.keyword_triggers:
            self.keyword_triggers[trigger]['keywords'].extend(variants)
    
    def process_agent_output(self, agent_id: str, message: str) -> Optional[str]:
        """
        Process agent output to trigger state transitions.
        
        Args:
            agent_id: Identifier for the agent
            message: The agent's output message
            
        Returns:
            New state if transition occurred, None otherwise
        """
        message_lower = message.lower()
        
        # Check each trigger for keywords
        for trigger, trigger_info in self.keyword_triggers.items():
            # Only consider triggers from current state
            if trigger_info['from_state'] != self.current_state:
                continue
            
            # Check if any keyword is in the message
            for keyword in trigger_info['keywords']:
                if keyword in message_lower:
                    # Transition found
                    old_state = self.current_state
                    self.current_state = trigger_info['to_state']
                    self.state_history.append({
                        'agent': agent_id,
                        'from': old_state,
                        'to': self.current_state,
                        'trigger': trigger,
                        'message': message[:100]  # Store snippet
                    })
                    
                    # Log transition
                    self._log_transition(agent_id, old_state, self.current_state, trigger)
                    
                    return self.current_state
        
        return None
    
    def _log_transition(self, agent_id: str, old_state: str, new_state: str, trigger: str):
        """Log state transition for monitoring."""
        print(f"[State Transition] Agent '{agent_id}': {old_state} -> {new_state} via '{trigger}'")
    
    def get_current_state(self) -> str:
        """Get current state of the state machine."""
        return self.current_state
    
    def get_available_triggers(self) -> List[str]:
        """Get available triggers from current state."""
        current_transitions = self.transition_table['transitions'].get(self.current_state, {})
        return list(current_transitions.keys())
    
    def is_final_state(self) -> bool:
        """Check if current state is final state."""
        return self.current_state == self.transition_table['final']
    
    def reset(self):
        """Reset state machine to initial state."""
        self.current_state = self.transition_table['initial']
        self.state_history = []
```

### 2. PLATO Room Integration Layer

```python
class PLATOStateAwareRoom:
    """
    PLATO room enhanced with state machine management.
    Coordinates multiple agents with state-based workflows.
    """
    
    def __init__(self, room_config: Dict, state_diagram: str):
        """
        Initialize state-aware PLATO room.
        
        Args:
            room_config: PLATO room configuration
            state_diagram: Mermaid state diagram string
        """
        self.room_config = room_config
        self.state_manager = AgentStateManager(state_diagram)
        self.agents = {}
        self.message_queue = []
        self.transition_handlers = {}
        
        # Initialize with example agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize agents based on room configuration."""
        # Example agent setup - would integrate with actual PLATO agent system
        self.agents = {
            'query_processor': {'type': 'processor', 'state': 'idle'},
            'tile_matcher': {'type': 'matcher', 'state': 'idle'},
            'llm_synthesizer': {'type': 'synthesizer', 'state': 'idle'},
            'response_builder': {'type': 'builder', 'state': 'idle'}
        }
    
    def register_transition_handler(self, from_state: str, to_state: str, handler_func):
        """
        Register custom handler for specific state transitions.
        
        Args:
            from_state: Starting state
            to_state: Target state
            handler_func: Function to call when transition occurs
        """
        key = (from_state, to_state)
        self.transition_handlers[key] = handler_func
    
    def process_agent_message(self, agent_id: str, message: str) -> Dict:
        """
        Process message from agent and handle state transitions.
        
        Args:
            agent_id: ID of the sending agent
            message: Message content
            
        Returns:
            Processing result with state information
        """
        # Add to message queue
        self.message_queue.append({
            'agent': agent_id,
            'message': message,
            'timestamp': time.time()
        })
        
        # Process for state transitions
        new_state = self.state_manager.process_agent_output(agent_id, message)
        
        result = {
            'agent': agent_id,
            'processed': True,
            'current_state': self.state_manager.get_current_state(),
            'state_changed': new_state is not None
        }
        
        # If state changed, execute transition handlers
        if new_state:
            old_state = self.state_manager.state_history[-1]['from'] if self.state_manager.state_history else None
            self._execute_transition_handlers(old_state, new_state, agent_id, message)
            
            # Update agent states based on new system state
            self._update_agent_states(new_state)
        
        return result
    
    def _execute_transition_handlers(self, old_state: str, new_state: str, agent_id: str, message: str):
        """Execute registered handlers for state transition."""
        key = (old_state, new_state)
        if key in self.transition_handlers:
            try:
                self.transition_handlers[key](agent_id, message, old_state, new_state)
            except Exception as e:
                print(f"Error in transition handler: {e}")
    
    def _update_agent_states(self, system_state: str):
        """Update individual agent states based on system state."""
        # Map system states to agent states
        state_mapping = {
            'Idle': {'query_processor':