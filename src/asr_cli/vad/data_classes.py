import dataclasses


@dataclasses.dataclass
class WindowBound:
    start_sample: int
    end_sample: int
