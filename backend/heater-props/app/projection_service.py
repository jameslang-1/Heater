# app/projection_service.py
# Service for loading pre-generated projections

import json
import os
from typing import List, Dict, Any, Optional

class ProjectionService:
    def __init__(self, projections_file='projections_cache.json'):
        self.projections_file = projections_file
        self.projections = {}
        self.load_projections()
    
    def load_projections(self):
        """Load projections from cache file"""
        if not os.path.exists(self.projections_file):
            print(f"Warning: Projections file not found: {self.projections_file}")
            return
        
        try:
            with open(self.projections_file, 'r') as f:
                self.projections = json.load(f)
            print(f"Loaded projections for {len(self.projections)} games")
        except Exception as e:
            print(f"Error loading projections: {e}")
            self.projections = {}
    
    def get_projections_for_game(self, game_id: str) -> List[Dict[str, Any]]:
        """Get projections for a specific game"""
        if game_id not in self.projections:
            return []
        
        return self.projections[game_id].get('projections', [])
    
    def get_all_projections(self) -> Dict[str, Any]:
        """Get all projections"""
        return self.projections
    
    def has_projections_for_game(self, game_id: str) -> bool:
        """Check if projections exist for a game"""
        return game_id in self.projections and len(self.projections[game_id].get('projections', [])) > 0

# Global instance
projection_service = ProjectionService()