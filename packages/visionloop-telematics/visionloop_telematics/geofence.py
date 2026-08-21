import math

class GeofenceEngine:
    """Geospatial boundary and perimeter validation using Haversine calculation."""
    
    @staticmethod
    def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes great-circle distance between two GPS points in Kilometers."""
        R = 6371.0 # Earth radius in km
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (
            math.sin(d_lat / 2.0) ** 2 +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(R * c, 3)
    
    @staticmethod
    def is_within_radius(
        current_lat: float,
        current_lng: float,
        center_lat: float = 28.6139,
        center_lng: float = 77.2090,
        radius_km: float = 80.0
    ) -> bool:
        """Returns True if current coordinates are within radius of designated center."""
        dist = GeofenceEngine.calculate_distance_km(current_lat, current_lng, center_lat, center_lng)
        return dist <= radius_km
