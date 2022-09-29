#this library is under development
#available libraries
#DHT11, SSD1306, WS2812, Analog Value, Buzzer with Tones
import machine
import array
import micropython
import utime, time
from machine import Pin, PWM
from micropython import const
import framebuf
import rp2
from math import ceil
 
       
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
    

########WS2812##########
class WS2812:
    """
    WS2812 driver class.
    
        
    Parameters
    --------------------
    pin : int
        GPIO number
    
    n : int
        Number of leds (default 1)
    
    brightness : float
        Percentage of brightness level (0.0~1.0, default 1.0)
    
    autowrite : bool
        Automatically call .show() whenever buffer is changed (default False)
    
    statemachine : int
        State machine id (0~7)
    """
    
    __slot__ = ['n', 'brightness', 'autowrite', 'buffer', '_sm']

    # PIO state machine assembly code
    @staticmethod
    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,
                 out_shiftdir=rp2.PIO.SHIFT_LEFT,
                 autopull=True, pull_thresh=24)
    def _ws2812():
        wrap_target()
        label('bitloop')
        out(x, 1)               .side(0)
        jmp(not_x, 'do_zero')   .side(1)
        jmp('bitloop')
        label('do_zero')
        nop()                   .side(0)
        wrap()

    def __init__(self, pin, n=1, brightness=1.0, autowrite=False, statemachine=1):
        self.brightness = brightness
        self.autowrite = autowrite
        self._sm = rp2.StateMachine(statemachine,
                                    WS2812._ws2812,
                                    freq=2400000,
                                    sideset_base=Pin(pin, Pin.OUT))
        self._sm.active(1)
        self.buffer = [(0, 0, 0)] * n
        if not self.autowrite:
            self.show()

    def __getitem__(self, key):
        return self.buffer[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.buffer[key] = tuple(value)
        elif isinstance(key, slice):
            self.buffer[key] = [tuple(color) for color in value]
        if self.autowrite:
            self.show()

    def __len__(self):
        return len(self.buffer)

    @property
    def n(self):
        return len(self.buffer)

    def fill(self, color):
        """
        Fill a specific color to all leds.
        
        Parameters
        --------------------
        color : list or tuple
            (r, g, b)
        """
        self[:] = [color] * self.n
        if self.autowrite:
            self.show()
    
    def clear(self):
        """
        Clear all leds.
        """
        self.fill((0, 0, 0))

    def rainbow_cycle(self, cycle=0):
        """
        Set rainbow colors accross all leds.
        
        Parameters
        --------------------
        cycle : int
            Cycle (0~255) of rainbow colors (default 0)
        """
        self[:] = [WS2812._wheel((round(i * 255 / self.n) + cycle) & 255) for i in range(self.n)]
        if self.autowrite:
            self.show()
            
    def rotate(self, clockwise=True):
        """
        Rotate current buffer clockwise or counter-clockwise.
        
        Parameters
        --------------------
        clockwise : bool
            Rotate counterwise (Default True; False = counter-clockwise)
        """
        self[:] = self[-1:] + self[:-1] if clockwise else self[1:] + self[:1]
        if self.autowrite:
            self.show()

    def show(self):
        """
        Write buffer to leds via state machine.
        """
        self.brightness = WS2812._between(self.brightness, 0.0, 1.0)
        uint16_arr = array.array('I', [0] * self.n)
        for i, color in enumerate(self.buffer):
            if not isinstance(color, tuple) or len(color) != 3:
                raise ValueError('Incorrect color data:' + str(color))
            r = WS2812._between(round(color[0] * self.brightness), 0, 255)
            g = WS2812._between(round(color[1] * self.brightness), 0, 255)
            b = WS2812._between(round(color[2] * self.brightness), 0, 255)
            uint16_arr[i] = (g << 16) | (r << 8) | b
        self._sm.put(uint16_arr, 8)
#        time.sleep_us(50)

    # for generating rainbow colors
    @staticmethod
    def _wheel(pos):
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    # for limiting a value between an interval
    @staticmethod
    def _between(value, minV, maxV):
        return max(min(value, maxV), minV)
