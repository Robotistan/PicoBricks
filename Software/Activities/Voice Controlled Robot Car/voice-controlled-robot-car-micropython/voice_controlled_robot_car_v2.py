import time
from machine import Pin, I2C, PWM, UART, time_pulse_us
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from picobricks import SSD1306_I2C, WS2812, NEC_16, IR_RX, MotorDriver

# ==================== CONFIGURATION ====================
WIDTH  = 128
HEIGHT = 64
OBSTACLE_CM = 15       # Obstacle detection distance (cm)
MOTOR_SPEED = 255      # Motor speed (0-255)
TURN_SPEED  = 200      # Turning speed (0-255)

# ==================== PIN DEFINITIONS ====================
BUZZER_PIN = 20
RGB_PIN    = 6
LED_PIN    = 7
IR_PIN     = 0
TRIG_PIN   = 15        # HC-SR04 Trigger pin
ECHO_PIN   = 14        # HC-SR04 Echo pin

# ==================== HARDWARE SETUP ====================
# I2C, OLED display, and motor driver
i2c  = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
motor = MotorDriver(i2c)

# RGB LED setup
ws2812 = WS2812(RGB_PIN, brightness=1)

# Buzzer setup
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty_u16(0)

# Single LED setup
led = Pin(LED_PIN, Pin.OUT)

# HC-SR04 ultrasonic sensor setup
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

uart_bt = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart_buffer = ""

# ==================== BLE SETUP ====================
ble_packets = []

ble = bluetooth.BLE()
ble.active(True)
ble.config(mtu=512)  # Large packet size (default is ~23 bytes, text was getting truncated)
sp = BLESimplePeripheral(ble, name="PB_Car")

def on_ble_rx(data):
    global ble_packets
    ble_packets.append(bytes(data))

sp.on_write(on_ble_rx)

# ==================== IR SETUP ====================
ir_data = 0
ir_received = False

def ir_callback(data, addr, ctrl):
    global ir_data, ir_received
    if data > 0:
        ir_data = data
        ir_received = True
        print('IR -> Data: 0x{:02x} Addr: 0x{:04x}'.format(data, addr))

ir = NEC_16(Pin(IR_PIN, Pin.IN), ir_callback)

# ==================== STATE VARIABLES ====================
is_moving_forward = False
last_ble_cmd = ""    # Last executed BLE command (prevents repeated execution)

# ==================== BUZZER FUNCTIONS ====================
def beep(duration_ms=100):
    # Play a short beep for the given duration
    buzzer.duty_u16(2000)
    buzzer.freq(1000)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

def beep_double():
    # Play two short beeps
    beep(100)
    time.sleep_ms(150)
    beep(100)

# ==================== RGB LED FUNCTIONS ====================
def set_rgb(r, g, b):
    # Set RGB LED to the given color
    ws2812.pixels_fill((r, g, b))
    ws2812.pixels_show()

def blink_rgb(r, g, b, times=3, delay_ms=200):
    # Blink RGB LED with the given color
    for _ in range(times):
        set_rgb(r, g, b)
        time.sleep_ms(delay_ms)
        set_rgb(0, 0, 0)
        time.sleep_ms(delay_ms)

# ==================== OLED DISPLAY FUNCTIONS ====================
def show_direction(tr_text, en_text):
    oled.fill(0)

    # Title
    oled.text("= PICOBRICKS =", 4, 0)

    # Turkish direction text (centered)
    tr_x = (128 - len(tr_text) * 8) // 2
    if tr_x < 0:
        tr_x = 0
    oled.text(tr_text, tr_x, 20)

    # English direction text (centered)
    en_x = (128 - len(en_text) * 8) // 2
    if en_x < 0:
        en_x = 0
    oled.text(en_text, en_x, 36)

    # Bottom information line
    oled.text("IR + BLE / VOICE", 0, 56)

    oled.show()

def show_obstacle(distance):
    # Display obstacle warning and measured distance
    oled.fill(0)
    oled.text("!! DIKKAT !!", 16, 0)
    oled.text("ENGEL!", 32, 20)
    oled.text("OBSTACLE!", 20, 36)
    oled.text("Distance: {} cm".format(int(distance)), 10, 56)
    oled.show()

# ==================== MOTOR CONTROL FUNCTIONS ====================
def forward(speed=MOTOR_SPEED):
    global is_moving_forward
    is_moving_forward = True
    motor.dc(1, speed, 0)
    motor.dc(2, speed, 0)
    show_direction("ILERI", "FORWARD")
    set_rgb(0, 255, 0)      # Green

def backward(speed=MOTOR_SPEED):
    global is_moving_forward
    is_moving_forward = False
    motor.dc(1, speed, 1)
    motor.dc(2, speed, 1)
    show_direction("GERI", "BACK")
    set_rgb(255, 0, 0)      # Red

def turn_right(speed=TURN_SPEED):
    global is_moving_forward
    is_moving_forward = False
    motor.dc(1, speed, 0)   # Left motor forward
    motor.dc(2, speed, 1)   # Right motor backward
    show_direction("SAG", "RIGHT")
    set_rgb(0, 0, 255)      # Blue

def turn_left(speed=TURN_SPEED):
    global is_moving_forward
    is_moving_forward = False
    motor.dc(1, speed, 1)   # Left motor backward
    motor.dc(2, speed, 0)   # Right motor forward
    show_direction("SOL", "LEFT")
    set_rgb(255, 255, 0)    # Yellow

def stop_motors():
    global is_moving_forward, last_ble_cmd
    is_moving_forward = False
    last_ble_cmd = "stop"  # Prevent the same BLE packet from triggering stop again
    motor.dc(1, 0, 0)
    motor.dc(2, 0, 0)
    show_direction("DUR", "STOP")
    set_rgb(0, 0, 0)

# ==================== HC-SR04 DISTANCE MEASUREMENT ====================
def measure_distance():
    # Send trigger pulse and measure echo response time
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    try:
        duration = time_pulse_us(echo, 1, 30000)
        if duration < 0:
            return 999.0
        return (duration * 0.0343) / 2.0
    except:
        return 999.0

def check_obstacle():
    global is_moving_forward
    # Only check for obstacles while moving forward
    if not is_moving_forward:
        return False
    dist = measure_distance()
    if 0 < dist < OBSTACLE_CM:
        stop_motors()
        show_obstacle(dist)
        blink_rgb(255, 0, 0, 3, 200)
        beep(300)
        return True
    return False

# ==================== BLE DATA PROCESSING HELPER FUNCTIONS ====================
def clean_ble_text(buf):
    # Keep only printable ASCII characters
    clean = ""
    for b in buf:
        if 32 <= b < 127:
            clean += chr(b)
    return clean.strip()

def find_last_direction(words):
    # Find the last valid direction keyword in the received words
    last_dir = None
    for word in words:
        w = word.lower()
        if "ileri" in w or "forward" in w:
            last_dir = "forward"
        elif "geri" in w or "backward" in w:
            last_dir = "backward"
        elif "back" in w and "play" not in w:
            last_dir = "backward"
        elif "sag" in w or "right" in w:
            last_dir = "right"
        elif "sol" in w or "left" in w:
            last_dir = "left"
        elif "dur" in w or "stop" in w:
            last_dir = "stop"
    return last_dir

def execute_direction(direction):
    """Execute the direction command"""
    if direction == "forward":
        forward()
    elif direction == "backward":
        backward()
    elif direction == "right":
        turn_right()
    elif direction == "left":
        turn_left()
    elif direction == "stop":
        stop_motors()

def process_ble_data():
    global ble_packets, last_ble_cmd

    if not ble_packets:
        return

    # Copy packet list and clear buffer
    packets = ble_packets[:]
    ble_packets = []

    current_text = ""
    for buf in packets:
        try:
            clean = clean_ble_text(buf)
            if clean:
                current_text = clean
        except:
            pass

    if not current_text:
        return

    words = current_text.lower().split()
    direction = find_last_direction(words)

    if not direction:
        return

    # Ignore repeated BLE commands
    if direction == last_ble_cmd:
        return

    last_ble_cmd = direction
    execute_direction(direction)

# ==================== UART BLUETOOTH PROCESSING ====================
def read_uart_bt():
    global uart_buffer
    while uart_bt.any():
        c = chr(uart_bt.read(1)[0])
        if c in ('\n', '\r'):
            word = uart_buffer.strip().lower()
            uart_buffer = ""
            if len(word) == 0:
                continue
            print("UART: \"{}\"".format(word))
            direction = find_last_direction([word])
            if direction:
                print(">> UART DIRECTION: " + direction)
                execute_direction(direction)
        else:
            uart_buffer += c
            # Reset buffer if input gets too long
            if len(uart_buffer) > 30:
                uart_buffer = ""

# ==================== IR REMOTE PROCESSING ====================
def process_ir():
    global ir_data, ir_received

    if not ir_received:
        return

    ir_received = False
    code = ir_data
    ir_data = 0

    if code == IR_RX.number_2:       # Forward
        forward()
    elif code == IR_RX.number_8:     # Backward
        backward()
    elif code == IR_RX.number_4:     # Left
        turn_left()
    elif code == IR_RX.number_6:     # Right
        turn_right()
    elif code == IR_RX.number_5:     # Stop
        stop_motors()
    elif code == IR_RX.number_ok:    # Stop (OK button)
        stop_motors()
    elif code == IR_RX.number_0:     # Stop (alternative)
        stop_motors()
    else:
        print("Undefined IR: 0x{:02x}".format(code))

# ==================== STARTUP SEQUENCE ====================
show_direction("HAZIR", "READY")
set_rgb(255, 255, 255)
beep(150)
time.sleep_ms(400)

# RGB LED startup color animation
set_rgb(0, 255, 0)     # Green
time.sleep_ms(250)
set_rgb(255, 0, 0)     # Red
time.sleep_ms(250)
set_rgb(0, 0, 255)     # Blue
time.sleep_ms(250)
set_rgb(255, 255, 0)   # Yellow
time.sleep_ms(250)
set_rgb(0, 0, 0)

# Blink onboard LED once
led.high()
time.sleep_ms(200)
led.low()

show_direction("DUR", "STOP")
beep_double()

last_obstacle_check = time.ticks_ms()
was_connected = False

# ==================== MAIN LOOP ====================
while True:
    connected = sp.is_connected()

    # Handle BLE connection state changes
    if connected and not was_connected:
        last_ble_word_count = 0
        last_ble_text = ""
        print("BLE connected")
    elif not connected and was_connected:
        last_ble_word_count = 0
        last_ble_text = ""
    was_connected = connected

    # Check obstacle distance every 100 ms
    now = time.ticks_ms()
    if time.ticks_diff(now, last_obstacle_check) >= 100:
        last_obstacle_check = now
        check_obstacle()

    # Process IR remote input
    process_ir()

    # Process BLE input only if connected
    if connected:
        process_ble_data()

    # Always process UART Bluetooth input
    read_uart_bt()

    # Small delay to reduce CPU usage
    time.sleep_ms(10)
