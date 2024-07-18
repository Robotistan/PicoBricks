import utime
import uos
import machine 
from machine import Pin, ADC, I2C
from picobricks import MotorDriver  
from utime import sleep 

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)
shtc_sensor = SHTC3(i2c)

smo_sensor=ADC(27)
motor.dc(1,0,0)

print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])

uart0 = machine.UART(0, baudrate=115200)
print(uart0)

def Connect_WiFi(cmd, uart=uart0, timeout=5000):
    print("CMD: " + cmd)
    uart.write(cmd)
    utime.sleep(7.0)
    Wait_ESP_Rsp(uart, timeout)
    print()
    
def Rx_ESP_Data():
    recv=bytes()
    while uart0.any()>0:
        recv+=uart0.read(1)
    res=recv.decode('utf-8')
    return res

def Send_AT_Cmd(cmd, uart=uart0, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    Wait_ESP_Rsp(uart, timeout)
    print()

def Wait_ESP_Rsp(uart=uart0, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)

Send_AT_Cmd('AT\r\n')          #Test AT startup
Send_AT_Cmd('AT+GMR\r\n')      #Check version information
Send_AT_Cmd('AT+CIPSERVER=0\r\n')   
Send_AT_Cmd('AT+RST\r\n')      #Check version information
Send_AT_Cmd('AT+RESTORE\r\n')  #Restore Factory Default Settings
Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the WiFi mode
Send_AT_Cmd('AT+CWMODE=1\r\n') #Set the WiFi mode = Station mode
Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the WiFi mode again
Send_AT_Cmd('AT+CWJAP="ID","Password"\r\n', timeout=5000) #Connect to AP
utime.sleep(3.0)
Send_AT_Cmd('AT+CIFSR\r\n')    #Obtain the Local IP Address
utime.sleep(3.0)
Send_AT_Cmd('AT+CIPMUX=1\r\n')    
utime.sleep(1.0)
Send_AT_Cmd('AT+CIPSERVER=1,80\r\n')    #Obtain the Local IP Address
utime.sleep(1.0)

while True:
    res =""
    res=Rx_ESP_Data()
    utime.sleep(2.0)
    if '+IPD' in res: # if the buffer contains IPD(a connection), then respond with HTML handshake
        id_index = res.find('+IPD')
        
        if '/WATERING' in res:
            print('Irrigation Start')
            motor.dc(1,255,0)
            utime.sleep(10)
            motor.dc(1,0,0)
            print('Irrigation Finished')
            connection_id =  res[id_index+5]
            print("connectionId:" + connection_id)
            print ('! Incoming connection - sending webpage')
            uart0.write('AT+CIPSEND='+connection_id+',200'+'\r\n')  
            utime.sleep(1.0)
            uart0.write('HTTP/1.1 200 OK'+'\r\n')
            uart0.write('Content-Type: text/html'+'\r\n')
            uart0.write('Connection: close'+'\r\n')
            uart0.write(''+'\r\n')
            uart0.write('<!DOCTYPE HTML>'+'\r\n')
            uart0.write('<html>'+'\r\n')
            uart0.write('<body><center><H1>CONNECTED...<br/></H1></center>'+'\r\n')
            uart0.write('<body><center><H1>Irrigation Complete.<br/></H1></center>'+'\r\n')
            uart0.write('</body></html>'+'\r\n')
        elif '/SERA' in res:
            temp = shtc_sensor.temperature()
            hum = shtc_sensor.humidity()
            smo = round((smo_sensor.read_u16()/65535)*100)
            sendStr="\"TEMP\":{}, \"Humidity\":{}, \"S.Moisture\":{}%".format(temp,hum,smo)
            sendText="{"+sendStr+"}"
            strLen=46+len(sendText)
            connection_id =  res[id_index+5]
            print("connectionId:" + connection_id)
            print ('! Incoming connection - sending webpage')
            atCmd="AT+CIPSEND="+connection_id+","+str(strLen)
            uart0.write(atCmd+'\r\n') 
            utime.sleep(1.0)
            uart0.write('HTTP/1.1 200 OK'+'\r\n')
            uart0.write('Content-Type: text/html'+'\r\n')
            uart0.write(''+'\r\n')
            uart0.write(sendText+'\r\n')
        elif '/' in res:        
            print("resp:")
            print(res)
            connection_id =  res[id_index+5]
            print("connectionId:" + connection_id)
            print ('! Incoming connection - sending webpage')
            uart0.write('AT+CIPSEND='+connection_id+',200'+'\r\n') 
            utime.sleep(3.0)
            uart0.write('HTTP/1.1 200 OK'+'\r\n')
            uart0.write('Content-Type: text/html'+'\r\n')
            uart0.write('Connection: close'+'\r\n')
            uart0.write(''+'\r\n')
            uart0.write('<!DOCTYPE HTML>'+'\r\n')
            uart0.write('<html>'+'\r\n')
            uart0.write('<body><center><H1>CONNECTED.<br/></H1></center>'+'\r\n')
            uart0.write('<center><h4>INFO:Get Sensor Data</br>WATERING:Run Water Pump</h4></center>'+'\r\n')
            uart0.write('</body></html>'+'\r\n')
        utime.sleep(4.0)
        Send_AT_Cmd('AT+CIPCLOSE='+ connection_id+'\r\n') # once file sent, close connection
        utime.sleep(3.0)
        recv_buf="" #reset buffer
        print ('Waiting For connection...')
