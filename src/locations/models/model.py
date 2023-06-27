class Location:

    def __init__(self, id: str|None = None, name: str | None = None, latitude: float | None = None, longitude: float | None = None ) -> None:
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
