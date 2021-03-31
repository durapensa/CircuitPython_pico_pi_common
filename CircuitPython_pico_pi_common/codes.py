# AUTOGENERATED! DO NOT EDIT! File to edit: 01_codes.ipynb (unless otherwise specified).

__all__ = ['ID_CODE', 'REG_CODE', 'REG_VAL_LEN', 'CMD_CATALOG', 'CMD_CODE', 'CMD_NAME', 'CMD_VAL_LEN',
           'REP_CLI_CATALOG', 'stats_struct']

# Cell

ID_CODE  = bytearray([ord(c) for c in list('ppdd')])
"""identifier string used by RPi(s) running PP device daemon"""

REG_CODE = {
    'CLR': bytearray([ord('F')]), # request to Flush/clear transmit FIFO
    'IDF': bytearray([ord('I')]), # request to send [str]  ID_CODE
    'BOS': bytearray([ord('B')]), # request to send [bool] Bosmang status
    'TIM': bytearray([ord('T')]), # request to send [int]  dateTime
    'CMD': bytearray([ord('C')]), # request to send [int]  Command
    'HOS': bytearray([ord('H')]), # request to send [str]  Hostname
    'LOD': bytearray([ord('L')]), # request to send [int]  Load
    'UPT': bytearray([ord('U')]), # request to send [int]  Uptime
    'TZN': bytearray([ord('Z')]), # request to send [int]  timeZone (sec offset from UTC)
    'PEN': bytearray([ord('P')]), # request to send [int]  MCU pin connected to RPi PEN

    'FLK': bytearray([ord('K')]), # command to flicker [int] PWR LED for seconds [int]
    'UID': bytearray([ord('V')]), # command to receive [int+bytearray] PPC len,microcontroller.cpu.uid
    'ICS': bytearray([ord('2')]), # command to receive [int+str] PPC len,I2C_str
    'MSG': bytearray([ord('M')]), # command to receive [int+str] message for display
    'REG': bytearray([ord('R')]), # command to receive [int+int+variable_len] PPD addr, REG_CODE, value
    'NAM': bytearray([ord('N')]), # command to receive [int+int+str] PPD addr,hostname (shorter than REG)
    'RPT': bytearray([ord('S')]), # command to receive [int] stats report data for N PPDs
    'PPD': bytearray([ord('D')]), # command to receive [int+int+str] PPD report addr,len,pack?
                                  # or use convention of R but send stored value without reg query
    'RBT': bytearray([247]),      # command to REBOOT
    'SDN': bytearray([248]),      # command to SHUTDOWN
    'ONN': bytearray([249]),      # command to POWERON
    'OFF': bytearray([250])}      # command to POWEROFF
"""I2C Register codes for PPDevices"""

REG_VAL_LEN = {# in bytes for first (sometimes only) read/write; + len for followon read/write
    'CLR': 16, # hardware transmit FIFO of RPi secondary I2C periph is 16 bytes
    'IDF': len(ID_CODE),
    'BOS': 1,  # len bosmang bool
    'TIM': 4,  # len timestamp int
    'CMD': 1,  # len cmd_code + bytes in CMD_CODE
    'HOS': 1,  # len len(hostname) + len(hostname)
    'LOD': 4,  # len loadavg string from float
    'UPT': 4,  # len uptime seconds int
    'TZN': 3,  # len utcoffset seconds int
    'PEN': 1,  # len pin int of MCU GPIO connected to PIN

    'FLK': 2,  # len cmd_code + duration int
    'UID': 1,  # len ACK + echo: len len(UID) + len(UID); set in PPController instance __init__
    'ICS': 1,  # len ACK + echo: len len(ICS) + len(ICS); set in PPController instance __init__
    'MSG': 1,  # len ACK + echo: len len(msg) + len(msg)
    'REG': 2,  # len ACK + echo: REG_CODE + REG_VALUE_LEN + len(REG value); for given register for given PPD
    'NAM': 2,  # len ACK + echo: len(hostname) + len(hostname); for given PPD
    'RPT': 1,  # len ACK + echo: len(ppds); ppds for which report data will be sent

    'RBT': 1,  # len ACK + echo: cmd_code + device_address
    'SDN': 1,  # len ACK + echo: cmd_code + device_address
    'ONN': 1,  # len ACK + echo: cmd_code + device_address
    'OFF': 1 } # len ACK + echo: cmd_code + device_address

CMD_CATALOG = (
    (  0, 'NOP',        0), # no command, not used
    ( 97, 'CONFIRM',    2), # device_address, cmd_code
    ( 99, 'OFFLINE',    1), # device_address
    ( 99, 'ONLINE',     1), # device_address
    (100, 'DEREGISTER', 1), # device_address
    (101, 'REG_GET' ,   2), # device_address, reg_code ; used for:
                            # hostname, bosmang, timezone, uart/gpio_poweroff/pen pins
                            # PPDevice will update its self values.
                            # ppdd must then accept incoming data addr+reg_code+value
                            # 2nd followon CONFIRM send when complete
    (122, 'FLICKER',    2), # device_address, duration

    (226, 'ROUNDROBIN', 1), # duration ; ALL PPDs
    (227, 'REPORT',     1), # number of ppds ; 0xFF for all; if not 0xFF,
                            # PPC then probes NAM register N times for list of addrs,
                            # hostname included for error detection.

    (247, 'REBOOT',     1), # device_address
    (248, 'SHUTDOWN',   1), # device_address
    (249, 'POWERON',    1), # device_address
    (250, 'POWEROFF',   1)) # device_address
"""
Command cmd_code int values, command NAME, number of bytes remaining in command.

All commands require followon CONFIRM.
All commands sending device_address may send 0xFF for ALL devices.
So as to avoid collisions with ASCII/UTF-8 control characters & capital letters
used by REG_CODE, purely to  avoid confusion, valid ranges are 97-122, 225-250.
Common commands (cmd_code <128) may be used by regular PPDs, but only on self.
Reserved commands (cmd_code >127) can be used externally only by bosmang.
Suggested for PPD to send OFFLNE before manual or programmed shutdown.
The number of PPDs that can be included in 'all' for POWERON & POWEROFF is
limited by the number of available MCU GPIOs for RPi-connected pins for
gpio_poweroff & PEN.
"""

CMD_CODE =    { }
CMD_NAME =    { }
CMD_VAL_LEN = { }

for code, name, vallen in CMD_CATALOG:
    CMD_CODE[name]=code
    CMD_NAME[code]=name
    CMD_VAL_LEN[code]=vallen

REP_CLI_CATALOG = (
    ('hostname', 'hostname'),
    ('mcu_uid', 'uid'),
    ('ppc_i2c_str', 'id'),
    ('device_address', 'address'),
    ('lastonline', 'lastonline'),
    ('loadavg', 'loadavg'),
    ('bosmang', 'bosmang'),
    ('utcoffset', 'timezone')
)

stats_struct = { }

for property_name, common_name in REP_CLI_CATALOG:
    stats_struct[name]=None