#this library is under development
#available libraries
#DHT11, SSD1306, WS2812, Analog Value, Buzzer with Tones, IR Receiver Author : peterhinch
import machine
import array
import micropython
import utime, time
from machine import Pin, PWM, Timer
from micropython import const
import framebuf
import rp2
from math import ceil
##########DHT11 Library##########
class InvalidChecksum(Exception):
    pass
 
class InvalidPulseCount(Exception):
    pass
 
MAX_UNCHANGED = const(100)
MIN_INTERVAL_US = const(200000)
HIGH_LEVEL = const(50)
EXPECTED_PULSES = const(84)
 
class DHT11:
    _temperature: float
    _humidity: float
 
    def __init__(self, pin):
        self._pin = pin
        self._last_measure = utime.ticks_us()
        self._temperature = -1
        self._humidity = -1
 
    def measure(self):
        current_ticks = utime.ticks_us()
        if utime.ticks_diff(current_ticks, self._last_measure) < MIN_INTERVAL_US and (
            self._temperature > -1 or self._humidity > -1
        ):
            # Less than a second since last read, which is too soon according
            # to the datasheet
            return
 
        self._send_init_signal()
        pulses = self._capture_pulses()
        buffer = self._convert_pulses_to_buffer(pulses)
        self._verify_checksum(buffer)
 
        self._humidity = buffer[0] + buffer[1] / 10
        self._temperature = buffer[2] + buffer[3] / 10
        self._last_measure = utime.ticks_us()
 
    @property
    def humidity(self):
        #self.measure()
        return self._humidity
 
    @property
    def temperature(self):
        #self.measure()
        return self._temperature
 
    def _send_init_signal(self):
        self._pin.init(Pin.OUT, Pin.PULL_DOWN)
        self._pin.value(1)
        utime.sleep_ms(50)
        self._pin.value(0)
        utime.sleep_ms(25)
 
    @micropython.native
    def _capture_pulses(self):
        pin = self._pin
        pin.init(Pin.IN, Pin.PULL_UP)
 
        val = 1
        idx = 0
        transitions = bytearray(EXPECTED_PULSES)
        unchanged = 0
        timestamp = utime.ticks_us()
 
        while unchanged < MAX_UNCHANGED:
            if val != pin.value():
                if idx >= EXPECTED_PULSES:
                    raise InvalidPulseCount(
                        "Got more than {} pulses".format(EXPECTED_PULSES)
                    )
                now = utime.ticks_us()
                transitions[idx] = now - timestamp
                timestamp = now
                idx += 1
                val = 1 - val
                unchanged = 0
            else:
                unchanged += 1
        pin.init(Pin.OUT, Pin.PULL_DOWN)
        if idx != EXPECTED_PULSES:
            raise InvalidPulseCount(
                "Expected {} but got {} pulses".format(EXPECTED_PULSES, idx)
            )
        return transitions[4:]
 
    def _convert_pulses_to_buffer(self, pulses):
        """Convert a list of 80 pulses into a 5 byte buffer
        The resulting 5 bytes in the buffer will be:
            0: Integral relative humidity data
            1: Decimal relative humidity data
            2: Integral temperature data
            3: Decimal temperature data
            4: Checksum
        """
        # Convert the pulses to 40 bits
        binary = 0
        for idx in range(0, len(pulses), 2):
            binary = binary << 1 | int(pulses[idx] > HIGH_LEVEL)
 
        # Split into 5 bytes
        buffer = array.array("B")
        for shift in range(4, -1, -1):
            buffer.append(binary >> shift * 8 & 0xFF)
        return buffer
 
    def _verify_checksum(self, buffer):
        # Calculate checksum
        checksum = 0
        for buf in buffer[0:4]:
            checksum += buf
        if checksum & 0xFF != buffer[4]:
            raise InvalidChecksum()
            
##########SSD1306 Library##########
set_contrast = const(0x81)
set_entire_on = const(0xA4)
set_norm_inv = const(0xA6)
set_disp = const(0xAE)
set_mem_addr = const(0x20)
set_color_addr = const(0x21)
set_page_addr = const(0x22)
set_disp_start_line = const(0x40)
set_seg_remap = const(0xA0)
set_mux_ratio = const(0xA8)
set_com_out_dir = const(0xC0)
set_disp_offset = const(0xD3)
set_com_pin_cfg = const(0xDA)
set_disp_clk_div = const(0xD5)
set_precharge = const(0xD9)
set_vcom_desel = const(0xDB)
set_charge_pump = const(0x8D)

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            set_disp | 0x00,  # off
            # address setting
            set_mem_addr,
            0x00,  # horizontal
            # resolution and layout
            set_disp_start_line | 0x00,
            set_seg_remap |0x001, # column addr 127 mapped to SEG0
            set_mux_ratio,
            self.height - 1,
            set_com_out_dir | 0x08,  # scan from COM[N] to COM0
            set_disp_offset,
            0x00,
            set_com_pin_cfg,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            set_disp_clk_div,
            0x80,
            set_precharge,
            0x22 if self.external_vcc else 0xF1,
            set_vcom_desel,
            0x30,  # 0.83*Vcc
            # display
            set_contrast,
            0xFF,  # maximum
            set_entire_on,  # output follows RAM contents
            set_norm_inv,  # not inverted
            # charge pump
            set_charge_pump,
            0x10 if self.external_vcc else 0x14,
            set_disp | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(set_disp | 0x00)

    def poweron(self):
        self.write_cmd(set_disp | 0x01)

    def contrast(self, contrast):
        self.write_cmd(set_contrast)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(set_norm_inv | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(set_color_addr)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(set_page_addr)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)
        

##########WS2812 Library##########
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

class WS2812():
    
    def __init__(self, num_leds=1, pin_num=6, brightness=0.2):
        self.num_leds = num_leds
        self.pin_num = pin_num
        self.brightness = brightness
        self.ar = array.array("I", [0 for _ in range(self.num_leds)])
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(self.pin_num))
        self.sm.active(1)

    ##########################################################################
    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.num_leds)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
        time.sleep_ms(10)

    def pixels_set(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

    def color_chase(self, color, wait):
        for i in range(self.num_leds):
            self.pixels_set(i, color)
            time.sleep(wait)
            self.pixels_show()
        time.sleep(0.2)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_leds):
                rc_index = (i * 256 // self.num_leds) + j
                self.pixels_set(i, self.wheel(rc_index & 255))
            self.pixels_show()
            time.sleep(wait)
        
##########Analog Value##########
conversion_factor = 3.3 / (65535)
class ReadADC():
    
    def __init__(self, pot_pin=26, ldr_pin=27):
        self.pot_pin=pot_pin
        self.ldr_pin=ldr_pin
        
    def read_potentiometer(self):
        potentiometer = machine.ADC(self.pot_pin)
        reading = potentiometer.read_u16() #Read Potentiometer ADC Value
        voltage = reading * conversion_factor #Read Potentiometer Voltage
        return reading, voltage
    
    def read_ldr(self):
        ldr = machine.ADC(self.ldr_pin)
        reading = ldr.read_u16() #Read LDR ADC Value
        voltage = reading * conversion_factor #Read LDR Voltage
        return reading, voltage

##########Buzzer with Tones##########
tones = {
    'C0':16,
    'C#0':17,
    'D0':18,
    'D#0':19,
    'E0':21,
    'F0':22,
    'F#0':23,
    'G0':24,
    'G#0':26,
    'A0':28,
    'A#0':29,
    'B0':31,
    'C1':33,
    'C#1':35,
    'D1':37,
    'D#1':39,
    'E1':41,
    'F1':44,
    'F#1':46,
    'G1':49,
    'G#1':52,
    'A1':55,
    'A#1':58,
    'B1':62,
    'C2':65,
    'C#2':69,
    'D2':73,
    'D#2':78,
    'E2':82,
    'F2':87,
    'F#2':92,
    'G2':98,
    'G#2':104,
    'A2':110,
    'A#2':117,
    'B2':123,
    'C3':131,
    'C#3':139,
    'D3':147,
    'D#3':156,
    'E3':165,
    'F3':175,
    'F#3':185,
    'G3':196,
    'G#3':208,
    'A3':220,
    'A#3':233,
    'B3':247,
    'C4':262,
    'C#4':277,
    'D4':294,
    'D#4':311,
    'E4':330,
    'F4':349,
    'F#4':370,
    'G4':392,
    'G#4':415,
    'A4':440,
    'A#4':466,
    'B4':494,
    'C5':523,
    'C#5':554,
    'D5':587,
    'D#5':622,
    'E5':659,
    'F5':698,
    'F#5':740,
    'G5':784,
    'G#5':831,
    'A5':880,
    'A#5':932,
    'B5':988,
    'C6':1047,
    'C#6':1109,
    'D6':1175,
    'D#6':1245,
    'E6':1319,
    'F6':1397,
    'F#6':1480,
    'G6':1568,
    'G#6':1661,
    'A6':1760,
    'A#6':1865,
    'B6':1976,
    'C7':2093,
    'C#7':2217,
    'D7':2349,
    'D#7':2489,
    'E7':2637,
    'F7':2794,
    'F#7':2960,
    'G7':3136,
    'G#7':3322,
    'A7':3520,
    'A#7':3729,
    'B7':3951,
    'C8':4186,
    'C#8':4435,
    'D8':4699,
    'D#8':4978,
    'E8':5274,
    'F8':5588,
    'F#8':5920,
    'G8':6272,
    'G#8':6645,
    'A8':7040,
    'A#8':7459,
    'B8':7902,
    'C9':8372,
    'C#9':8870,
    'D9':9397,
    'D#9':9956,
    'E9':10548,
    'F9':11175,
    'F#9':11840,
    'G9':12544,
    'G#9':13290,
    'A9':14080,
    'A#9':14917,
    'B9':15804
}

#Time, Note, Duration, Instrument (onlinesequencer.net schematic format)
#0 D4 8 0;0 D5 8 0;0 G4 8 0;8 C5 2 0;10 B4 2 0;12 G4 2 0;14 F4 1 0;15 G4 17 0;16 D4 8 0;24 C4 8 0

class music:
    def __init__(self, songString='0 D4 8 0', looping=True, tempo=3, duty=2512, pin=None, pins=[Pin(0)]):
        self.tempo = tempo
        self.song = songString
        self.looping = looping
        self.duty = duty
        
        self.stopped = False
        
        self.timer = -1
        self.beat = -1
        self.arpnote = 0
        
        self.pwms = []
        
        if (not (pin is None)):
            pins = [pin]
            
        i = 0
        for pin in pins:
            self.pwms.append(PWM(pins[i]))
            i = i + 1
        
        self.notes = []

        self.playingNotes = []
        self.playingDurations = []


        #Find the end of the song
        self.end = 0
        splitSong = self.song.split(";")
        for note in splitSong:
            snote = note.split(" ")
            testEnd = round(float(snote[0])) + ceil(float(snote[2]))
            if (testEnd > self.end):
                self.end = testEnd
                
        #Create empty song structure
        while (self.end > len(self.notes)):
            self.notes.append(None)

        #Populate song structure with the notes
        for note in splitSong:
            snote = note.split(" ")
            beat = round(float(snote[0]));
            
            if (self.notes[beat] == None):
                self.notes[beat] = []
            self.notes[beat].append([snote[1],ceil(float(snote[2]))]) #Note, Duration


        #Round up end of song to nearest bar
        self.end = ceil(self.end / 8) * 8
    
    def stop(self):
        for pwm in self.pwms:
            pwm.deinit()
        self.stopped = True
        
    def tick(self):
        if (not self.stopped):
            self.timer = self.timer + 1
            
            #Loop
            if (self.timer % (self.tempo * self.end) == 0 and (not (self.timer == 0))):
                if (not self.looping):
                    self.stop()
                    return False
                self.beat = -1
                self.timer = 0
            
            #On Beat
            if (self.timer % self.tempo == 0):
                self.beat = self.beat + 1

                #Remove expired notes from playing list
                i = 0
                while (i < len(self.playingDurations)):
                    self.playingDurations[i] = self.playingDurations[i] - 1
                    if (self.playingDurations[i] <= 0):
                        self.playingNotes.pop(i)
                        self.playingDurations.pop(i)
                    else:
                        i = i + 1
                        
                #Add new notes and their durations to the playing list
                
                """
                #Old method runs for every note, slow to process on every beat and causes noticeable delay
                ssong = song.split(";")
                for note in ssong:
                    snote = note.split(" ")
                    if int(snote[0]) == beat:
                        playingNotes.append(snote[1])
                        playingDurations.append(int(snote[2]))
                """
                
                if (self.beat < len(self.notes)):
                    if (self.notes[self.beat] != None):
                        for note in self.notes[self.beat]:
                            self.playingNotes.append(note[0])
                            self.playingDurations.append(note[1])
                
                #Only need to run these checks on beats
                i = 0
                for pwm in self.pwms:
                    if (i >= len(self.playingNotes)):
                        pwm.duty_u16(0)
                    else:
                        #Play note
                        pwm.duty_u16(self.duty)
                        pwm.freq(tones[self.playingNotes[i]])
                    i = i + 1
            

            #Play arp of all playing notes
            if (len(self.playingNotes) > len(self.pwms)):
                self.pwms[len(self.pwms)-1].duty_u16(self.duty)
                if (self.arpnote > len(self.playingNotes)-len(self.pwms)):
                    self.arpnote = 0
                self.pwms[len(self.pwms)-1].freq(tones[self.playingNotes[self.arpnote+(len(self.pwms)-1)]])
                self.arpnote = self.arpnote + 1
                
            return True
        else:
            return False
##########IR Reciever Library##########

class IR_RX():
    # Result/error codes
    # Repeat button code
    REPEAT = -1
    # Error codes
    BADSTART = -2
    BADBLOCK = -3
    BADREP = -4
    OVERRUN = -5
    BADDATA = -6
    BADADDR = -7

    def __init__(self, pin, nedges, tblock, callback, *args):  # Optional args for callback
        self._pin = pin
        self._nedges = nedges
        self._tblock = tblock
        self.callback = callback
        self.args = args
        self._errf = lambda _ : None
        self.verbose = False

        self._times = array.array('i',  (0 for _ in range(nedges + 1)))  # +1 for overrun
        pin.irq(handler = self._cb_pin, trigger = (Pin.IRQ_FALLING | Pin.IRQ_RISING))
        self.edge = 0
        self.tim = Timer(-1)  # Sofware timer
        self.cb = self.decode

    # Pin interrupt. Save time of each edge for later decode.
    def _cb_pin(self, line):
        t = utime.ticks_us()
        # On overrun ignore pulses until software timer times out
        if self.edge <= self._nedges:  # Allow 1 extra pulse to record overrun
            if not self.edge:  # First edge received
                self.tim.init(period=self._tblock , mode=Timer.ONE_SHOT, callback=self.cb)
            self._times[self.edge] = t
            self.edge += 1

    def do_callback(self, cmd, addr, ext, thresh=0):
        self.edge = 0
        if cmd >= thresh:
            self.callback(cmd, addr, ext, *self.args)
        else:
            self._errf(cmd)

    def error_function(self, func):
        self._errf = func

    def close(self):
        self._pin.irq(handler = None)
        self.tim.deinit()


class NEC_ABC(IR_RX):
    def __init__(self, pin, extended, callback, *args):
        # Block lasts <= 80ms (extended mode) and has 68 edges
        super().__init__(pin, 68, 80, callback, *args)
        self._extended = extended
        self._addr = 0

    def decode(self, _):
        try:
            if self.edge > 68:
                raise RuntimeError(self.OVERRUN)
            width = utime.ticks_diff(self._times[1], self._times[0])
            if width < 4000:  # 9ms leading mark for all valid data
                raise RuntimeError(self.BADSTART)
            width = utime.ticks_diff(self._times[2], self._times[1])
            if width > 3000:  # 4.5ms space for normal data
                if self.edge < 68:  # Haven't received the correct number of edges
                    raise RuntimeError(self.BADBLOCK)
                # Time spaces only (marks are always 562.5µs)
                # Space is 1.6875ms (1) or 562.5µs (0)
                # Skip last bit which is always 1
                val = 0
                for edge in range(3, 68 - 2, 2):
                    val >>= 1
                    if utime.ticks_diff(self._times[edge + 1], self._times[edge]) > 1120:
                        val |= 0x80000000
            elif width > 1700: # 2.5ms space for a repeat code. Should have exactly 4 edges.
                raise RuntimeError(self.REPEAT if self.edge == 4 else self.BADREP)  # Treat REPEAT as error.
            else:
                raise RuntimeError(self.BADSTART)
            addr = val & 0xff  # 8 bit addr
            cmd = (val >> 16) & 0xff
            if cmd != (val >> 24) ^ 0xff:
                raise RuntimeError(self.BADDATA)
            if addr != ((val >> 8) ^ 0xff) & 0xff:  # 8 bit addr doesn't match check
                if not self._extended:
                    raise RuntimeError(self.BADADDR)
                addr |= val & 0xff00  # pass assumed 16 bit address to callback
            self._addr = addr
        except RuntimeError as e:
            cmd = e.args[0]
            addr = self._addr if cmd == self.REPEAT else 0  # REPEAT uses last address
        # Set up for new data burst and run user callback
        self.do_callback(cmd, addr, 0, self.REPEAT)

class NEC_8(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, False, callback, *args)

class NEC_16(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, callback, *args)