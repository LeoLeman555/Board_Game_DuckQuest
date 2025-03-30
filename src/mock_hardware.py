class ButtonManager:
    """Mock ButtonManager for non-Raspberry Pi systems."""

    def __init__(self, pins):
        print("[MOCK] ButtonManager initialized with pins:", pins)

    def get_pressed_button(self):
        return None

    def cleanup(self):
        print("[MOCK] ButtonManager cleanup.")


class LEDStripManager:
    """Mock LEDStripManager for non-Raspberry Pi systems."""

    def clear(self):
        print("[MOCK] LED Strip cleared.")

    def blink(self, color, times, delay):
        print(f"[MOCK] Blinking LED {times} times with color {color}.")

    def score_effect(self, score):
        return "[MOCK] Score effect color"
