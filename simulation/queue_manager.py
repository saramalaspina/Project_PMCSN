import random
from collections import deque


class QueueManager:
    def __init__(self):
        self.queues = {
            "edge_node": deque(),
            "cloud_server": deque()
        }

    def validate_queue(self, type):
        if type not in self.queues:
            raise ValueError(f"Error: Invalid type '{type}'")
        return True

    def add_to_queue(self, type, job_time):
        if self.validate_queue(type):
            self.queues[type].append(job_time)

    def get_from_queue(self, type):
        if self.validate_queue(type) and self.queues[type]:
            return self.queues[type].popleft()
        return None

    def is_queue_empty(self, type):
        if self.validate_queue(type):
            return len(self.queues[type]) == 0

    def get_queue_length(self, type):
        if self.validate_queue(type):
            return len(self.queues[type])

    def reset_queues(self):
        for key, queue in self.queues.items():
            queue.clear()

    def check_queues(self):
        for key, queue in self.queues.items():
            if len(queue) != 0:
                return False
        return True