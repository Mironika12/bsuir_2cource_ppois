class MusicPlaylist:
    """
    Простой плейлист для фоновой музыки в зале.
    """
    def __init__(self, name: str, tracks: list[str] = None):
        self._name = name
        self._tracks = tracks or []
        self._current = 0

    def add_track(self, track: str):
        self._tracks.append(track)

    def next_track(self) -> str | None:
        if not self._tracks:
            return None
        self._current = (self._current + 1) % len(self._tracks)
        return self._tracks[self._current]

    def get_current(self) -> str | None:
        if not self._tracks:
            return None
        return self._tracks[self._current]

    def get_info(self) -> dict:
        return {"name": self._name, "tracks": list(self._tracks), "current_index": self._current}
