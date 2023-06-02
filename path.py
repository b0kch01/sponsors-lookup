class Path:
    def __init__(self, path: str):
        self.path = path

    def __truediv__(self, other):
        if type(other) is Path:
            return Path(f'{self.path}/{other.path}')

        other.removeprefix('/')
        return Path(f'{self.path}/{other}')

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f'Path({self.path})'
