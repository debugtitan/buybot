from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(i.value, i.name) for i in cls]

    @classmethod
    def values(cls):
        return list(i.value for i in cls)

    @classmethod
    def count(cls):
        return len(cls)

    @classmethod
    def mapping(cls):
        return dict((i.name, i.value) for i in cls)


class ProgramIdType(BaseEnum):
    RAYDIUM_POOL = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
    TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    META_DATA_PROGRAM = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    WRAPPED_SOL = "So11111111111111111111111111111111111111112"