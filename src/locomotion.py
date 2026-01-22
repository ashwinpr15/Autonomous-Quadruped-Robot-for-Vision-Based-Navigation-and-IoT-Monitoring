import time
from threading import Thread
import Adafruit_PCA9685

# Servo Driver Config
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

# Gait Angles
FRONT_PARALLEL = 90
FRONT_LATERAL = 140
BACK_PARALLEL = 90
BACK_LATERAL = 40
FOOT_UP = 0
FOOT_DOWN = 60

# Joint Mappings (3 servos per leg)
LEG1 = [0, 1, 2] 
LEG2 = [3, 4, 5]
LEG3 = [6, 7, 8]
LEG4 = [9, 10, 11]

def move_servo(channel, start_angle, end_angle):
    """ Smoothly actuates servo to prevent torque spikes. """
    step = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle, step):
        pulse = int((angle * 2.5) + 150)
        pwm.set_pwm(channel, 0, pulse)
        time.sleep(0.005)

def forward_gait():
    """ Executes 'Creep Gait' cycle for forward motion. """
    print("Executing Forward Creep Gait...")
    # Sequence: Lift Leg 1 -> Swing -> Drop -> Repeat for others
    move_servo(LEG1[1], FOOT_DOWN, FOOT_UP)     # Lift
    move_servo(LEG1[0], FRONT_PARALLEL, FRONT_LATERAL) # Swing
    move_servo(LEG1[1], FOOT_UP, FOOT_DOWN)     # Drop
    time.sleep(0.1)
    # (Full sequence would continue for other legs)

def backward_gait():
    print("Executing Backward Creep Gait...")
    # Inverse sequence logic
