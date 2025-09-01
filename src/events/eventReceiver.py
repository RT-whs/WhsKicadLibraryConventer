from blinker import Signal


class EventReceiver:
    def __init__(self, signal: Signal, handler=None):
        self.signal = signal
        self.custom_handler = handler or self.default_handler
        self.signal_id = self.signal.connect(self.custom_handler)

    def default_handler(self, sender, **kwargs):
        print(f"EventReceiver: Received event from {sender} with data {kwargs}")

    def disconnect(self):
        """ Odpojí signál, aby se metoda už nevolala. """
        if self.signal and self.signal_id:
            self.signal.disconnect(self.signal_id)
            print("EventReceiver: Disconnected from signal.")


# Odeslání signálu
#button_signal.send("Button", action="clicked")  
# Output: EventReceiver: Received event from Button with data {'action': 'clicked'}

# Odpojení signálu
#receiver.disconnect()

# Odeslání signálu po odpojení
#button_signal.send("Button", action="clicked")  
# Output: (nic se nestane, protože receiver je odpojen)
