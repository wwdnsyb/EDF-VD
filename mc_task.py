class MCTask:
    def __init__(self, *args):
        if len(args) == 4:
            if isinstance(args[0], list):
                self.C = [int(x) for x in args[0]]
            elif isinstance(args[0], (int, float)):
                self.C = [int(args[0]), int(args[1])]
            self.T = int(args[1])
            if isinstance(args[2], list):
                self.D = args[2]
            else:
                self.D = [int(args[2])] * len(self.C)
            self.L = int(args[3])
            if any(x < 0 for x in self.C) or self.T <= 0 or any(x < 0 for x in self.D) or self.L not in [0, 1]:
                raise ValueError("Invalid task parameters")
        elif len(args) == 1 and isinstance(args[0], str):
            params = args[0].split(" ")
            self.C = [int(params[0]), int(params[1])]
            self.T = int(params[2])
            self.D = [int(params[3]), int(params[4])]
            self.L = int(params[5])
            if any(x < 0 for x in self.C) or self.T <= 0 or any(x < 0 for x in self.D) or self.L not in [0, 1]:
                raise ValueError("Invalid task parameters")

    def get_wcet(self, level):
        return self.C[level]

    def get_t(self):
        return self.T

    def get_d(self, index=None):
        if index is None:
            return self.D[-1]
        return self.D[index]

    def get_d_l(self, l):
        return self.D[l]

    def set_d(self, l, val):
        self.D[l] = val

    def get_l(self):
        return self.L

    def __str__(self):
        return f"[{self.C}, {self.T}, {self.D}, {self.L}]"

    def get_wcet_list(self):
        return self.C

    def __hash__(self):
        return hash((tuple(self.C), tuple(self.D), self.L, self.T))

    def __eq__(self, other):
        if isinstance(other, MCTask):
            return self.C == other.C and self.D == other.D and self.L == other.L and self.T == other.T
        return False