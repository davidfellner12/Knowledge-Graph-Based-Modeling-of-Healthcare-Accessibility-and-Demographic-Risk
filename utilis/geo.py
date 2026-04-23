from geopy.distance import geodesic


class GeoEngine:
    def __init__(self, hospitals_df):
        self.hospitals = hospitals_df

    def nearest_hospital(self, lat, lon):
        min_dist = float("inf")

        for _, h in self.hospitals.iterrows():
            dist = geodesic((lat, lon), (h["lat"], h["lon"])).km
            min_dist = min(min_dist, dist)

        return {"distance_km": min_dist}