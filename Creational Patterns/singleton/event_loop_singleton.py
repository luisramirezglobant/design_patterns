import asyncio

class EventLoopSingleton:
    event_loop = None

    def get_event_loop(self):
        if self.event_loop is None:
            self.event_loop = asyncio.new_event_loop()
        return self.event_loop
    
event_loop_singleton = EventLoopSingleton()
loop = event_loop_singleton.get_event_loop()