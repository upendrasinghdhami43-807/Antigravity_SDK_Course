from typing import List, Dict, Optional, Tuple
from app.logger import get_logger
from app.settings import SettingsManager

logger = get_logger("ModelManager")

class ModelManager:
    def __init__(self, client, settings_mgr: SettingsManager):
        self.client = client
        self.settings_mgr = settings_mgr
        self._available_models = []
        self._categorized_models = {}
        self._indexed_models = {}

    def load_available_models(self) -> List[str]:
        if not self.client:
            return []
        if self._available_models:
            return self._available_models
            
        try:
            # Get all text generation models that are likely to be used
            models = self.client.models.list()
            
            # Allow all gemini models
            self._available_models = [
                m.name for m in models if "gemini" in m.name.lower()
            ]
            
            self._categorize_models()
            logger.debug(f"Loaded {len(self._available_models)} models from API.")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self._available_models = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"]
            self._categorize_models()
        
        return self._available_models
        
    def _categorize_models(self):
        categories = {
            "General / Fast (Free Tier Friendly)": [],
            "Complex Reasoning (Pro)": [],
            "Image & Vision": [],
            "Audio & Voice": [],
            "Embeddings & Search": [],
            "Preview & Experimental (May be Paid)": [],
            "Other": []
        }
        
        # Build category lists
        for model in self._available_models:
            name = model.lower()
            if "embedding" in name:
                categories["Embeddings & Search"].append(model)
            elif "image" in name or "vision" in name:
                categories["Image & Vision"].append(model)
            elif "audio" in name or "tts" in name:
                categories["Audio & Voice"].append(model)
            elif "preview" in name or "omni" in name or "gemini-3" in name:
                categories["Preview & Experimental (May be Paid)"].append(model)
            elif "pro" in name:
                categories["Complex Reasoning (Pro)"].append(model)
            elif "flash" in name:
                categories["General / Fast (Free Tier Friendly)"].append(model)
            else:
                categories["Other"].append(model)
                
        # Build flat indexed dictionary for number selection
        self._categorized_models = {k: v for k, v in categories.items() if v}
        self._indexed_models = {}
        
        idx = 1
        for category, models in self._categorized_models.items():
            for m in models:
                self._indexed_models[str(idx)] = m
                idx += 1

    def get_categorized_models(self) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
        if not self._categorized_models:
            self.load_available_models()
        return self._categorized_models, self._indexed_models

    def get_current_model(self) -> str:
        return self.settings_mgr.get("current_model", "gemini-2.0-flash")

    def switch_model(self, new_model_input: str) -> bool:
        self.load_available_models() # Ensure models are loaded
        
        # Check if the input is an index
        if new_model_input in self._indexed_models:
            actual_model = self._indexed_models[new_model_input]
            self.settings_mgr.set("current_model", actual_model)
            logger.info(f"Switched model via index to {actual_model}")
            return True
            
        # Check if it's a direct model name
        if new_model_input in self._available_models:
            self.settings_mgr.set("current_model", new_model_input)
            logger.info(f"Switched model to {new_model_input}")
            return True
            
        # Check if they just missed the 'models/' prefix
        if f"models/{new_model_input}" in self._available_models:
            self.settings_mgr.set("current_model", f"models/{new_model_input}")
            logger.info(f"Switched model to models/{new_model_input}")
            return True
            
        logger.warning(f"Attempted to switch to invalid model: {new_model_input}")
        return False
