import time
from threading import Thread, Lock
import Adafruit_PCA9685

# --- Configuration from Project Report ---
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
i2c_mutex = Lock()

# Servo Pulse Limits
SERVO_MIN = 150
SERVO_MAX = 600
MOVE_DELAY = 0.005
STEP_DELAY = 0.01

# Gait Angles (Calibrated)
FRONT_PARALLEL = 90
FRONT_LATERAL = 140
FRONT_LATERAL_ADD = -30
BACK_PARALLEL = 90
BACK_LATERAL = 40
BACK_LATERAL_ADD = 30
FOOT_UP = 0
FOOT_DOWN = 60
PINCER_UP = 130
PINCER_DOWN = 120

# Calibration Offsets (from PDF Page 6)
LEG1_OFFSET = [5, 5, 0]
LEG2_OFFSET = [5, 0, 0]
LEG3_OFFSET = [0, 7, 0]
LEG4_OFFSET = [-5, -5, 5]

# Global State
leg_formation = 0
channel_cur = [90] * 12  # Current angles of all 12 servos

def set_servo(channel, angle):
    """Standard servo movement."""
    angle = max(0, min(180, angle))
    with i2c_mutex:
        pulse = int((angle * 2.5) + 150)
        pwm.set_pwm(channel, 0, pulse)

def set_servo_invert(channel, angle):
    """Inverted servo movement for opposing legs."""
    angle = max(0, min(180, angle))
    with i2c_mutex:
        pulse = int((angle * -2.5) + 600)
        pwm.set_pwm(channel, 0, pulse)

def move_leg_servos(leg_index, target_angles, offsets, invert_indices=[]):
    """
    Moves 3 servos of a specific leg to target angles.
    leg_index: 0=Leg1, 3=Leg2, 6=Leg3, 9=Leg4 (Start Channel)
    """
    angles_with_offset = [t + o for t, o in zip(target_angles, offsets)]

    # Simple P-Controller style movement loop
    while True:
        moved = False
        for i in range(3):
            channel = leg_index + i
            target = angles_with_offset[i]
            current = channel_cur[channel]

            if current != target:
                moved = True
                step = 1 if target > current else -1
                channel_cur[channel] += step

                if channel in invert_indices:
                    set_servo_invert(channel, channel_cur[channel])
                else:
                    set_servo(channel, channel_cur[channel])

        if not moved:
            break
        time.sleep(MOVE_DELAY)

# --- Threaded Leg Wrappers (Matches PDF Pages 24-28) ---
def leg1(a1, a2, a3):
    # Leg 1: Channels 0,1,2 (0 & 1 Inverted)
    move_leg_servos(0, [a1, a2, a3], LEG1_OFFSET, invert_indices=[0, 1])

def leg2(a1, a2, a3):
    # Leg 2: Channels 3,4,5 (3 & 4 Inverted)
    move_leg_servos(3, [a1, a2, a3], LEG2_OFFSET, invert_indices=[3, 4])

def leg3(a1, a2, a3):
    # Leg 3: Channels 6,7,8 (8 Inverted)
    move_leg_servos(6, [a1, a2, a3], LEG3_OFFSET, invert_indices=[8])

def leg4(a1, a2, a3):
    # Leg 4: Channels 9,10,11 (11 Inverted)
    move_leg_servos(9, [a1, a2, a3], LEG4_OFFSET, invert_indices=[11])

# --- High Level Gaits ---
def begin():
    """Initializes Robot Stance (Page 9)"""
    global leg_formation
    print("Initializing Stance...")

    t1 = Thread(target=leg1, args=(FRONT_PARALLEL, FOOT_DOWN, PINCER_DOWN))
    t2 = Thread(target=leg2, args=(BACK_PARALLEL, FOOT_DOWN, PINCER_DOWN))
    t3 = Thread(target=leg3, args=(BACK_LATERAL, FOOT_DOWN, PINCER_DOWN))

    t1.start(); t2.start(); t3.start()
    leg4(FRONT_LATERAL, FOOT_DOWN, PINCER_DOWN) # Run Leg4 on main thread

    t1.join(); t2.join(); t3.join()
    leg_formation = 1
    print("Ready.")

def forward():
    """Creep Gait Forward Logic (Page 10-13)"""
    global leg_formation
    print(f"Moving Forward (State {leg_formation})")

    if leg_formation == 1:
        # 1. Lift Leg 1 -> Swing Lateral -> Drop
        leg1(FRONT_PARALLEL, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg1(FRONT_LATERAL, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg1(FRONT_LATERAL, FOOT_DOWN, PINCER_DOWN)
        time.sleep(STEP_DELAY)

        # 2. Push Body: Leg2(Lat), Leg3(Lat+), Leg4(Par)
        t2 = Thread(target=leg2, args=(BACK_LATERAL, FOOT_DOWN, PINCER_DOWN))
        t3 = Thread(target=leg3, args=(BACK_LATERAL + BACK_LATERAL_ADD, FOOT_DOWN, PINCER_DOWN))
        t4 = Thread(target=leg4, args=(FRONT_PARALLEL, FOOT_DOWN, PINCER_DOWN))
        t2.start(); t3.start(); t4.start()
        t2.join(); t3.join(); t4.join()

        # 3. Lift Leg 3 -> Swing Parallel -> Drop
        leg3(BACK_LATERAL + BACK_LATERAL_ADD, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg3(BACK_PARALLEL, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg3(BACK_PARALLEL, FOOT_DOWN, PINCER_DOWN)

        leg_formation = 2

    elif leg_formation == 2:
        # Similar logic for State 2 (Leg 4 and Leg 2 movement)
        # ... (Implementation mirrors state 1 logic from PDF)
        leg4(FRONT_PARALLEL, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg4(FRONT_LATERAL, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg4(FRONT_LATERAL, FOOT_DOWN, PINCER_DOWN)

        t3 = Thread(target=leg3, args=(BACK_LATERAL, FOOT_DOWN, PINCER_DOWN))
        t2 = Thread(target=leg2, args=(BACK_LATERAL + BACK_LATERAL_ADD, FOOT_DOWN, PINCER_DOWN))
        t1 = Thread(target=leg1, args=(FRONT_PARALLEL, FOOT_DOWN, PINCER_DOWN))
        t3.start(); t2.start(); t1.start()
        t3.join(); t2.join(); t1.join()

        leg2(BACK_LATERAL + BACK_LATERAL_ADD, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg2(BACK_PARALLEL, FOOT_UP, PINCER_UP)
        time.sleep(STEP_DELAY)
        leg2(BACK_PARALLEL, FOOT_DOWN, PINCER_DOWN)

        leg_formation = 1

if __name__ == "__main__":
    try:
        begin()
        forward()
    except KeyboardInterrupt:
        print("Stopping.")
