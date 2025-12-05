# app/cache_manager.py
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import threading
import json
import os

class CacheManager:
    def __init__(self, cache_duration_hours: int = 12):
        """
        Initialize cache manager
        
        Args:
            cache_duration_hours: How long to keep cached data before refreshing
        """
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache = {}
        self.cache_file = 'data_cache.json'
        self.lock = threading.Lock()
        
        # Load existing cache from file if it exists
        self._load_cache_from_file()
    
    def _load_cache_from_file(self):
        """Load cache from JSON file on startup"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    file_data = json.load(f)
                    # Convert ISO strings back to datetime objects
                    for key, value in file_data.items():
                        if 'timestamp' in value:
                            value['timestamp'] = datetime.fromisoformat(value['timestamp'])
                    self.cache = file_data
                    print(f"Loaded cache from {self.cache_file}")
            except Exception as e:
                print(f"Error loading cache file: {e}")
                self.cache = {}
    
    def _save_cache_to_file(self):
        """Save cache to JSON file for persistence"""
        try:
            # Convert datetime objects to ISO strings for JSON serialization
            file_data = {}
            for key, value in self.cache.items():
                file_data[key] = {
                    'data': value['data'],
                    'timestamp': value['timestamp'].isoformat()
                }
            
            with open(self.cache_file, 'w') as f:
                json.dump(file_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache file: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached data if it exists and is still fresh
        
        Args:
            key: Cache key
            
        Returns:
            Cached data if fresh, None if expired or doesn't exist
        """
        with self.lock:
            if key not in self.cache:
                return None
            
            cached_item = self.cache[key]
            timestamp = cached_item['timestamp']
            data = cached_item['data']
            
            # Check if cache is still fresh
            if datetime.now() - timestamp < self.cache_duration:
                age_hours = (datetime.now() - timestamp).total_seconds() / 3600
                print(f"Cache hit for '{key}' (age: {age_hours:.1f} hours)")
                return data
            else:
                age_hours = (datetime.now() - timestamp).total_seconds() / 3600
                print(f"Cache expired for '{key}' (age: {age_hours:.1f} hours)")
                return None
    
    def set(self, key: str, data: Any):
        """
        Store data in cache with current timestamp
        
        Args:
            key: Cache key
            data: Data to cache
        """
        with self.lock:
            self.cache[key] = {
                'data': data,
                'timestamp': datetime.now()
            }
            print(f"Cached '{key}' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Save to file for persistence
            self._save_cache_to_file()
    
    def is_stale(self, key: str) -> bool:
        """
        Check if cached data exists but is stale
        
        Args:
            key: Cache key
            
        Returns:
            True if data exists but is expired
        """
        with self.lock:
            if key not in self.cache:
                return False
            
            timestamp = self.cache[key]['timestamp']
            return datetime.now() - timestamp >= self.cache_duration
    
    def clear(self, key: Optional[str] = None):
        """
        Clear cache for a specific key or all keys
        
        Args:
            key: Specific key to clear, or None to clear all
        """
        with self.lock:
            if key:
                if key in self.cache:
                    del self.cache[key]
                    print(f"Cleared cache for '{key}'")
            else:
                self.cache = {}
                print("Cleared all cache")
            
            self._save_cache_to_file()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about cached items
        
        Returns:
            Dictionary with cache statistics
        """
        with self.lock:
            info = {}
            for key, value in self.cache.items():
                timestamp = value['timestamp']
                age = datetime.now() - timestamp
                age_hours = age.total_seconds() / 3600
                
                info[key] = {
                    'cached_at': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'age_hours': round(age_hours, 1),
                    'is_fresh': age < self.cache_duration,
                    'expires_in_hours': round((self.cache_duration.total_seconds() / 3600) - age_hours, 1)
                }
            
            return info

# Global cache instance
cache_manager = CacheManager(cache_duration_hours=12)