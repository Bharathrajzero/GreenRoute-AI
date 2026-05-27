class IntentClassifier:
    def __init__(self):
        self.complex_indicators = ["execute", "optimize", "architect", "compile", "evaluate", "benchmark"]

    def evaluate(self, prompt: str) -> str:
        word_count = len(prompt.split())
        
        # Scenario 1: Extended text input size checks
        if word_count > 35:
            return "COMPLEX"
            
        # Scenario 2: High-cognitive task indicators
        if any(indicator in prompt.lower() for indicator in self.complex_indicators):
            return "COMPLEX"
            
        return "SIMPLE"
