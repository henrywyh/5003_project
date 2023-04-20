import threading
import time
import signal

class Terminator:    
    def on_stop_handler(self,signum, frame):
        raise KeyboardInterrupt

    def listen_stop_signal(self):
        signal.signal(signal.SIGINT, self.on_stop_handler)
        signal.signal(signal.SIGTERM, self.on_stop_handler)

class FlaskThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__( target=target, args=args)
        self.target = target
        self.args = args
        self.stop_event = threading.Event()
        self.terminator = Terminator()
        self.daemon = True
        self.start()

    def run(self):
        self.target(*self.args)
    def stop(self):        
        self.stop_event.set()
    
    def stopped(self):
        return self.stop_event.is_set()
     
    def stop_and_join(self):
        self.stop()
        if self.is_alive():
            self.join()