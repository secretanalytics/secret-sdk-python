from dataclasses import dataclass
import betterproto


@dataclass(eq=False, repr=False)
class EmptyRequest(betterproto.Message):
    pass
