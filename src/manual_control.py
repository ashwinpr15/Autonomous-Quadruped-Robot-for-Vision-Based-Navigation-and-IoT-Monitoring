import sys, tty, termios
from locomotion import begin, forward

# The report describes backward and turning gaits (Figs 5.7-5.9), but their code
# isn't part of this repository yet, so those keys explain that instead of crashing.
NOT_YET = "Not in this version yet: only the forward creep gait is implemented."

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
    print("Manual Control Active. [W] Forward  [X] Exit   (S/A/D: not implemented yet)")

    while True:
        char = get_key()

        if char == 'w':
            forward()
        elif char == 's':
            print(NOT_YET)
        elif char == 'a':
            print(NOT_YET)
        elif char == 'd':
            print(NOT_YET)
        elif char == 'x':
            print("Exiting...")
            break

if __name__ == "__main__":
    manual_drive()
