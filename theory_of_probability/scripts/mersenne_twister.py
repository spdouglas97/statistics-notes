from dataclasses import dataclass


@dataclass(frozen=True)
class MersenneTwisterParams:
    w: int
    n: int
    m: int
    r: int
    a: int
    b: int
    c: int
    f: int
    u: int
    s: int
    t: int
    l: int


class MersenneTwister:
    def __init__(self, seed: int, params: MersenneTwisterParams):
        self.params = params
        self.word_mask = (1 << params.w) - 1
        self.lower_mask = (1 << params.r) - 1
        self.upper_mask = self.word_mask ^ self.lower_mask
        self.state = [0] * params.n
        self.index = params.n
        self.state[0] = seed & self.word_mask

        for i in range(1, params.n):
            prev = self.state[i - 1]
            mixed = prev ^ (prev >> (params.w - 2))
            self.state[i] = (params.f * mixed + i) & self.word_mask

    def twist(self) -> None:
        for i in range(self.params.n):
            y = ((self.state[i] & self.upper_mask)
                 | (self.state[(i + 1) % self.params.n] & self.lower_mask))
            x_a = y >> 1
            if y & 1:
                x_a ^= self.params.a
            self.state[i] = self.state[(i + self.params.m) % self.params.n] ^ x_a
            self.state[i] &= self.word_mask
        self.index = 0

    def temper(self) -> int:
        if self.index >= self.params.n:
            self.twist()

        y = self.state[self.index]
        y ^= y >> self.params.u
        y ^= (y << self.params.s) & self.params.b
        y ^= (y << self.params.t) & self.params.c
        y ^= y >> self.params.l

        self.index += 1
        return y & self.word_mask

    def rand(self, n: int) -> list[float]:
        if n < 0:
            raise ValueError("n must be non-negative")
        scale = 1 << self.params.w
        return [self.temper() / scale for _ in range(n)]
