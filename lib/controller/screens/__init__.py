FILE_DATA_LEN = 16

PORT_OPEN = True
PORT_CLOSE = False

CAN_PKT_DATA_LEN = 13
CAN_DEFAULT_PKT_LEN = 15
CAN_TAG = CAN_RESERVED = 0
CAN_HEAD = 170
CAN_TAIL = 85
CAN_DATA_LEN = 200
FLASH_COUNT = 8


first_byte = lambda ele: ele % 256
second_byte = lambda ele: int(ele / 256)

# [170, 232, 8, 0, 0, 0, 83, 84, 79, 80, 32, 77, 65, 78, 85]

"""
    Packets to be sent to Controller unit
"""

# Connect Packet
"""
    CanId : 9 (0x09)
    Packet : [1, 0, 0, 0, 0, 0, 0, 0]
"""

CONNECT_PCKT = [
    CAN_HEAD, CAN_DATA_LEN, 9, CAN_TAG, CAN_TAG, CAN_TAG,
    1, 0, 0, 0, 0, 0, 0, 0,
    CAN_TAIL
]

"""
    CanId : 0x236 (566)
    
    ack: [170,  200,    54,     2,     71,     101,    110,    101,    114,    97,     116,    101,    85]
         [Head, Len,    CanId,  CanId, D1,      D2,     D3,     D4,     D5,     D6,      D7,     D8,    Tail]
    
    Can Id Value Calculation
    54, 2
    2 * 256 = 512
    54 + 512 = 566
"""

connect_ack = [170, 200, 54, 2, 71, 101, 110, 101, 114, 97, 116, 101, 85]
# connect_ack = [170, 200, 36, 2, 71, 101, 110, 101, 114, 97, 116, 101, 85]

init_flash_pckt = [170, 200, 1, 0, 83, 84, 79, 80, 32, 77, 65, 78, 85]
init_flash_ack = [170, 200, 54, 2, 83, 119, 105, 116, 99, 104, 32, 112, 85]

eof_pckt = [170, 200, 8, 0, 71, 101, 110, 101, 114, 97, 116, 101, 85]

flash_ack = [170, 200, 54, 2, 83, 101, 110, 100, 32, 110, 101, 120, 85]

#############################################
# Error Codes
#############################################

PORT_DISCONNECTED_ABRUPTLY = 100
PORT_NOT_FOUND = 101
FLASH_BIN_DIALOG_CLOSED = 102
POWER_ON = 103

FLASHED_SUCCESSFULLY = 200
