class MovingAvg():
    def __init__(self, size: float):
        self.data = []
        self.size = size
        self.cur_index = 0
        self.avg = 0
        for _ in range(size):
            self.data.append(0)

    def insert(self, value: float):
        self.data[self.cur_index] = value
        self.cur_index = (self.cur_index + 1) % self.size
        self.avg = round(sum(self.data) / self.size, 2)

    def __repr__(self):
        return f"{self.size} - {self.avg}"

    def __str__(self):
        return self.__repr__()
