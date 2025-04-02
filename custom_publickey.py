class PublicKey:
    def __init__(self, key: str):
        self.key = key

    @classmethod
    def from_string(cls, key: str):
        return cls(key)

    def __str__(self):
        return self.key

    def __repr__(self):
        return f"PublicKey({self.key})"
