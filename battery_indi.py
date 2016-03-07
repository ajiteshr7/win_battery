import time
import ctypes
from ctypes import wintypes
from os import system

marker = "--------------------------"
# To store the variable provided by windows

def win_pop(msg):

    MessageBox = ctypes.windll.user32.MessageBoxA
    MessageBox(None, msg,'Battery Status', 0)

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ExternalPower', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD)
        ]

SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL

status = SYSTEM_POWER_STATUS()
if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise cytpes.WinError()

def disp_status():
    print marker
    print time.ctime()
    print marker
    if status.ExternalPower == 0:
        print "Using Battery"
    else:
        print "Charging"
    x_min = status.BatteryLifeTime / 60
    x_hr = x_min / 60
    if status.BatteryLifePercent < 25:
        cur = "Warning :: Battery getting low"
        print cur
        print "Current Status :: %r%% " % (status.BatteryLifePercent)
        print "Will last only %d hrs %d mins" % (x_hr,x_min % 60)
        win_pop(cur)
        print marker
    else:
        print "Sufficient Power :)"
        print "Current Status :: %r%% " % (status.BatteryLifePercent)
        print "Will last %d hrs %d mins" % (x_hr,x_min % 60)
        print marker
    system("pause")
# TODO write a func to write this info periodically

while status.ExternalPower == 0:
    disp_status()
    time.sleep(5)
# print 'ExternalPower', status.ExternalPower
# print 'BatteryFlag', status.BatteryFlag
# print 'BatteryLifePercent', status.BatteryLifePercent
# print 'BatteryLifeTime', status.BatteryLifeTime
