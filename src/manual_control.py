import sys, tty, termios
from locomotion import begin, forward, backward, turn_left, turn_right

def get_key():
    """Captures single keypress for real-time control (Page 8)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def manual_drive():
    print("Initializing Robot...")
    begin() # Set initial stance
    print("Manual Control Active. [W]Fwd [S]Bwd [A]Left [D]Right [X]Exit")

    while True:
        char = get_key()

        if char == 'w':
            forward()
        elif char == 's':
            backward() # Note: backward() needs to be implemented in locomotion.py similar to forward()
            print("Moving Backward")
        elif char == 'a':
            turn_left() # Note: turn_left() needs implementation
        elif char == 'd':
            turn_right() # Note: turn_right() needs implementation
        elif char == 'x':
            print("Exiting...")
            break

if __name__ == "__main__":
    manual_drive()
