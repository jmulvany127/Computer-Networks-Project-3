class Queue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)
    
    def is_empty(buffer):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)