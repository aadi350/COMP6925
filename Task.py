# Custom class for defining a 'Task'

class Task:
    def __init__(self, id, priority, clk_cycles):
        self.id = id
        self.priority = priority
        self.cycles = clk_cycles
        self.freq = None
        self.time = None

    def __str__(self):
        return str(self.id) + ' ' + str(self.priority) + ' ' + str(self.cycles)  + ' ' + str(self.freq)

    def __repr__(self):
        return str(self.id) + ' ' + str(self.priority) + ' ' + str(self.cycles) + ' ' + str(self.freq)

    def set_processor(self, freq):
        self.freq = freq
        self.time = self.cycles/freq

    def get_time(self):
        return self.time

    def get(self):
        return [self.id, self.priority, self.cycles, self.time]
