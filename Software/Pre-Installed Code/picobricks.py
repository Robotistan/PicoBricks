#this library is under development
#available libraries
#DHT11, SSD1306, WS2812, Analog Value, Buzzer with Tones, IR Receiver Author : peterhinch
import machine
import array
import micropython
import utime, time
from machine import Pin, PWM, Timer, SPI
from micropython import const
import framebuf
import rp2
from math import ceil
from os import uname

##########Motor Driver Library##########
class MotorDriver:
    def __init__(self, i2c):
        self.i2c = i2c
        
    def servo(self, servoNumber, angle):
        buf = bytearray(5)
        buf[0] = 0x26
        buf[1] = servoNumber + 2
        buf[2] = 0
        buf[3] = angle
        buf[4] = buf[1] ^ buf[2] ^ buf[3]
        self.i2c.writeto(0x22,buf, False)
        
    def dc(self, dcNumber, speed, direction):
        buf = bytearray(5)
        buf[0] = 0x26
        buf[1] = dcNumber
        buf[2] = speed
        buf[3] = direction
        buf[4] = buf[1] ^ buf[2] ^ buf[3]
        self.i2c.writeto(0x22,buf, False)
    
##########SHTC3 Library##########
class SHTC3:
    def __init__(self, i2c):
        buf = bytearray(2)
        buf1 = bytearray(3)
        
        self.i2c = i2c
        buf[0] = 0x35
        buf[1] = 0x17
        self.i2c.writeto(0x70,buf, False)
        time.sleep_ms(500)
        buf[0] = 0xEF
        buf[1] = 0xC8
        self.i2c.writeto(0x70,buf, False)
        time.sleep_ms(500)
        self.i2c.readfrom_into(0x70,buf1, True)
        
    def temperature(self):
        buf = bytearray(2)
        buf1 = bytearray(2)
        
        buf[0] = 0x78
        buf[1] = 0x66
        self.i2c.writeto(0x70, buf, False)
        time.sleep_ms(100)
        self.i2c.readfrom_into(0x70, buf1, True)
        time.sleep_ms(100)
        _temperature = ((buf1[0] << 8) | buf1[1])
        _temperature = (((4375 * _temperature) >> 14) - 4500) / 100
        return _temperature
    
    def humidity(self):
        buf = bytearray(2)
        buf1 = bytearray(5)
        
        buf[0] = 0x78
        buf[1] = 0x66
        self.i2c.writeto(0x70, buf, False)
        time.sleep_ms(100)
        self.i2c.readfrom_into(0x70, buf1, True)
        time.sleep_ms(100)
        _humidity = ((buf1[3] << 8) | buf1[4])
        _humidity = ((625 * _humidity) >> 12) / 100
        return _humidity
 
##########MFRC522##########
class MFRC522:
    DEBUG = False
    OK = 0
    NOTAGERR = 1
    ERR = 2
 
    REQIDL = 0x26
    REQALL = 0x52
    AUTHENT1A = 0x60
    AUTHENT1B = 0x61
  
    PICC_ANTICOLL1 = 0x93
    PICC_ANTICOLL2 = 0x95
    PICC_ANTICOLL3 = 0x97
 
    def __init__(self, sck, mosi, miso, rst, cs,baudrate=1000000,spi_id=0):
 
        self.sck = Pin(sck, Pin.OUT)
        self.mosi = Pin(mosi, Pin.OUT)
        self.miso = Pin(miso)
        self.rst = Pin(rst, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
 
        self.rst.value(0)
        self.cs.value(1)
        
        board = uname()[0]
 
        if board == 'WiPy' or board == 'LoPy' or board == 'FiPy':
            self.spi = SPI(0)
            self.spi.init(SPI.MASTER, baudrate=1000000, pins=(self.sck, self.mosi, self.miso))
        elif (board == 'esp8266') or (board == 'esp32'):
            self.spi = SPI(baudrate=100000, polarity=0, phase=0, sck=self.sck, mosi=self.mosi, miso=self.miso)
            self.spi.init()
        elif board == 'rp2':
            self.spi = SPI(spi_id,baudrate=baudrate,sck=self.sck, mosi= self.mosi, miso= self.miso)
        else:
            raise RuntimeError("Unsupported platform")
 
        self.rst.value(1)
        self.init()
 
    def _wreg(self, reg, val):
 
        self.cs.value(0)
        self.spi.write(b'%c' % int(0xff & ((reg << 1) & 0x7e)))
        self.spi.write(b'%c' % int(0xff & val))
        self.cs.value(1)
 
    def _rreg(self, reg):
 
        self.cs.value(0)
        self.spi.write(b'%c' % int(0xff & (((reg << 1) & 0x7e) | 0x80)))
        val = self.spi.read(1)
        self.cs.value(1)
 
        return val[0]
 
    def _sflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)
 
    def _cflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & (~mask))
 
    def _tocard(self, cmd, send):
 
        recv = []
        bits = irq_en = wait_irq = n = 0
        stat = self.ERR
 
        if cmd == 0x0E:
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == 0x0C:
            irq_en = 0x77
            wait_irq = 0x30
 
        self._wreg(0x02, irq_en | 0x80)
        self._cflags(0x04, 0x80)
        self._sflags(0x0A, 0x80)
        self._wreg(0x01, 0x00)
 
        for c in send:
            self._wreg(0x09, c)
        self._wreg(0x01, cmd)
 
        if cmd == 0x0C:
            self._sflags(0x0D, 0x80)
 
        i = 2000
        while True:
            n = self._rreg(0x04)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & wait_irq)):
                break
 
        self._cflags(0x0D, 0x80)
 
        if i:
            if (self._rreg(0x06) & 0x1B) == 0x00:
                stat = self.OK
 
                if n & irq_en & 0x01:
                    stat = self.NOTAGERR
                elif cmd == 0x0C:
                    n = self._rreg(0x0A)
                    lbits = self._rreg(0x0C) & 0x07
                    if lbits != 0:
                        bits = (n - 1) * 8 + lbits
                    else:
                        bits = n * 8
 
                    if n == 0:
                        n = 1
                    elif n > 16:
                        n = 16
 
                    for _ in range(n):
                        recv.append(self._rreg(0x09))
            else:
                stat = self.ERR
 
        return stat, recv, bits
 
    def _crc(self, data):
 
        self._cflags(0x05, 0x04)
        self._sflags(0x0A, 0x80)
 
        for c in data:
            self._wreg(0x09, c)
 
        self._wreg(0x01, 0x03)
 
        i = 0xFF
        while True:
            n = self._rreg(0x05)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break
 
        return [self._rreg(0x22), self._rreg(0x21)]
 
    def init(self):
 
        self.reset()
        self._wreg(0x2A, 0x8D)
        self._wreg(0x2B, 0x3E)
        self._wreg(0x2D, 30)
        self._wreg(0x2C, 0)
        self._wreg(0x15, 0x40)
        self._wreg(0x11, 0x3D)
        self.antenna_on()
 
    def reset(self):
        self._wreg(0x01, 0x0F)
 
    def antenna_on(self, on=True):
 
        if on and ~(self._rreg(0x14) & 0x03):
            self._sflags(0x14, 0x03)
        else:
            self._cflags(0x14, 0x03)
 
    def request(self, mode):
 
        self._wreg(0x0D, 0x07)
        (stat, recv, bits) = self._tocard(0x0C, [mode])
 
        if (stat != self.OK) | (bits != 0x10):
            stat = self.ERR
 
        return stat, bits
  
    def anticoll(self,anticolN):
 
        ser_chk = 0
        ser = [anticolN, 0x20]
 
        self._wreg(0x0D, 0x00)
        (stat, recv, bits) = self._tocard(0x0C, ser)
 
        if stat == self.OK:
            if len(recv) == 5:
                for i in range(4):
                    ser_chk = ser_chk ^ recv[i]
                if ser_chk != recv[4]:
                    stat = self.ERR
            else:
                stat = self.ERR
 
        return stat, recv
    
    def PcdSelect(self, serNum,anticolN):
        backData = []
        buf = []
        buf.append(anticolN)
        buf.append(0x70)
        #i = 0
        ###xorsum=0;
        for i in serNum:
            buf.append(i)
        #while i<5:
        #    buf.append(serNum[i])
        #    i = i + 1
        pOut = self._crc(buf)
        buf.append(pOut[0])
        buf.append(pOut[1])
        (status, backData, backLen) = self._tocard( 0x0C, buf)
        if (status == self.OK) and (backLen == 0x18):
            return  1
        else:
            return 0
    
    def SelectTag(self, uid):
        byte5 = 0
        
        #(status,puid)= self.anticoll(self.PICC_ANTICOLL1)
        #print("uid",uid,"puid",puid)
        for i in uid:
            byte5 = byte5 ^ i
        puid = uid + [byte5]
        
        if self.PcdSelect(puid,self.PICC_ANTICOLL1) == 0:
            return (self.ERR,[])
        return (self.OK , uid)
        
    def tohexstring(self,v):
        s="["
        for i in v:
            if i != v[0]:
                s = s+ ", "
            s=s+ "0x{:02X}".format(i)
        s= s+ "]"
        return s

    def SelectTagSN(self):
        valid_uid=[]
        (status,uid)= self.anticoll(self.PICC_ANTICOLL1)
        #print("Select Tag 1:",self.tohexstring(uid))
        if status != self.OK:
            return  (self.ERR,[])
        
        if self.DEBUG:   print("anticol(1) {}".format(uid))
        if self.PcdSelect(uid,self.PICC_ANTICOLL1) == 0:
            return (self.ERR,[])
        if self.DEBUG:   print("pcdSelect(1) {}".format(uid))
        
        #check if first byte is 0x88
        if uid[0] == 0x88 :
            #ok we have another type of card
            valid_uid.extend(uid[1:4])
            (status,uid)=self.anticoll(self.PICC_ANTICOLL2)
            #print("Select Tag 2:",self.tohexstring(uid))
            if status != self.OK:
                return (self.ERR,[])
            if self.DEBUG: print("Anticol(2) {}".format(uid))
            rtn =  self.PcdSelect(uid,self.PICC_ANTICOLL2)
            if self.DEBUG: print("pcdSelect(2) return={} uid={}".format(rtn,uid))
            if rtn == 0:
                return (self.ERR,[])
            if self.DEBUG: print("PcdSelect2() {}".format(uid))
            #now check again if uid[0] is 0x88
            if uid[0] == 0x88 :
                valid_uid.extend(uid[1:4])
                (status , uid) = self.anticoll(self.PICC_ANTICOLL3)
                #print("Select Tag 3:",self.tohexstring(uid))
                if status != self.OK:
                    return (self.ERR,[])
                if self.DEBUG: print("Anticol(3) {}".format(uid))
                if self.MFRC522_PcdSelect(uid,self.PICC_ANTICOLL3) == 0:
                    return (self.ERR,[])
                if self.DEBUG: print("PcdSelect(3) {}".format(uid))
        valid_uid.extend(uid[0:5])
        # if we are here than the uid is ok
        # let's remove the last BYTE whic is the XOR sum
        
        return (self.OK , valid_uid[:len(valid_uid)-1])
        #return (self.OK , valid_uid)

    def auth(self, mode, addr, sect, ser):
        return self._tocard(0x0E, [mode, addr] + sect + ser[:4])[0]
    
    def authKeys(self,uid,addr,keyA=None, keyB=None):
        status = self.ERR
        if keyA is not None:
            status = self.auth(self.AUTHENT1A, addr, keyA, uid)
        elif keyB is not None:
            status = self.auth(self.AUTHENT1B, addr, keyB, uid)
        return status
       
    def stop_crypto1(self):
        self._cflags(0x08, 0x08)
 
    def read(self, addr):
 
        data = [0x30, addr]
        data += self._crc(data)
        (stat, recv, _) = self._tocard(0x0C, data)
        return stat, recv
 
    def write(self, addr, data):
 
        buf = [0xA0, addr]
        buf += self._crc(buf)
        (stat, recv, bits) = self._tocard(0x0C, buf)
 
        if not (stat == self.OK) or not (bits == 4) or not ((recv[0] & 0x0F) == 0x0A):
            stat = self.ERR
        else:
            buf = []
            for i in range(16):
                buf.append(data[i])
            buf += self._crc(buf)
            (stat, recv, bits) = self._tocard(0x0C, buf)
            if not (stat == self.OK) or not (bits == 4) or not ((recv[0] & 0x0F) == 0x0A):
                stat = self.ERR
        return stat
 
    def writeSectorBlock(self,uid, sector, block, data, keyA=None, keyB = None):
        absoluteBlock =  sector * 4 + (block % 4)
        if absoluteBlock > 63 :
            return self.ERR
        if len(data) != 16:
            return self.ERR
        if self.authKeys(uid,absoluteBlock,keyA,keyB) != self.ERR :
            return self.write(absoluteBlock, data)
        return self.ERR
 
    def readSectorBlock(self,uid ,sector, block, keyA=None, keyB = None):
        absoluteBlock =  sector * 4 + (block % 4)
        if absoluteBlock > 63 :
            return self.ERR, None
        if self.authKeys(uid,absoluteBlock,keyA,keyB) != self.ERR :
            return self.read(absoluteBlock)
        return self.ERR, None
 
    def MFRC522_DumpClassic1K(self,uid, Start=0, End=64, keyA=None, keyB=None):
        for absoluteBlock in range(Start,End):
            status = self.authKeys(uid,absoluteBlock,keyA,keyB)
            # Check if authenticated
            print("{:02d} S{:02d} B{:1d}: ".format(absoluteBlock, absoluteBlock//4 , absoluteBlock % 4),end="")
            if status == self.OK:                    
                status, block = self.read(absoluteBlock)
                if status == self.ERR:
                    break
                else:
                    for value in block:
                        print("{:02X} ".format(value),end="")
                    print("  ",end="")
                    for value in block:
                        if (value > 0x20) and (value < 0x7f):
                            print(chr(value),end="")
                        else:
                            print('.',end="")
                    print("")
            else:
                break
        if status == self.ERR:
            print("Authentication error")
            return self.ERR
        return self.OK
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
    
    number_1 = 0x45
    number_2 = 0x46
    number_3 = 0x47
    number_4 = 0x44
    number_5 = 0x40
    number_6 = 0x43
    number_7 = 0x07
    number_8 = 0x15
    number_9 = 0x09
    number_0 = 0x19
    number_ok = 0x1c
    number_up = 0x18
    number_down = 0x52
    number_right = 0x5a
    number_left = 0x08
    number_star= 0x16
    number_sharp= 0x0d
    
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
        if self.edge > 68 :
            self.edge = 0

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
