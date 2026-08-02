from core.context.context_builder import Context

class PromptBuilder:
    """Combines all prompt pieces (system, developer, persona, memory, history, current) into one."""
    
    def build(self, context: Context, output_instructions: str = "") -> str:
        parts = []
        
        if context.system_prompt:
            parts.append("--- SYSTEM INSTRUCTIONS ---")
            parts.append(context.system_prompt)
            
        if context.developer_prompt:
            parts.append("--- DEVELOPER INSTRUCTIONS ---")
            parts.append(context.developer_prompt)
            
        if context.persona:
            parts.append("--- PERSONA ---")
            parts.append(context.persona)
            
        if context.memory and any(context.memory.values()):
            parts.append("--- USER MEMORY ---")
            import json
            parts.append(json.dumps(context.memory, indent=2))
            
        if context.history:
            parts.append("--- CONVERSATION HISTORY ---")
            for msg in context.history:
                parts.append(f"{msg.role}: {msg.content}")
                
        if output_instructions:
            parts.append("--- OUTPUT INSTRUCTIONS ---")
            parts.append(output_instructions)
            
        parts.append("--- USER INPUT ---")
        parts.append(context.question)
        
        return "\n\n".join(parts)
