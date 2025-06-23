class MapService:
    def __init__(self, widget):
        self.widget = widget
        self.markers = []

    def add_marker(self, lat: float, lon: float, label: str = ""):
        marker = self.widget.set_marker(lat, lon, text=label)
        self.markers.append(marker)
        return marker

    def remove_marker(self, marker):
        marker.delete()
        if marker in self.markers:
            self.markers.remove(marker)
