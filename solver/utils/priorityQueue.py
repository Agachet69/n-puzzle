class PriorityQueue:
    def __init__(self):
        self.list = []

    def add(self, priority, state, cost, parent):
        # self.list.append((priority, state, cost, parent))
        self.list.append({"priority":priority, "state":state, "cost":cost, "parent":parent})
        # self.list.sort(reverse=True)

    def pop(self):
        if self.list:
            value = min(self.list, key=lambda x: x['priority'])
            index = self.list.index(value)

            return self.list.pop(index).values()
        else:
            return None

    def is_empty(self):
        return len(self.list) == 0