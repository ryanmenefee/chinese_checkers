# -*- coding: utf-8 -*-
"""
Defines class objects for creating and parsing serial communication strings.

Created on Sat Apr 23 16:32:45 2022

@author: rmene
"""

import serial

def main():
    # Make a board state string as a test
    serial_board_state = SerialStringBoardState('<0,0,0,0;0,-1,1,0;1,-1,0,0;1,0,-1,0>')
    serial_board_state.print_serial_string()
    
    # Make a move string as a test
    serial_move = SerialStringMove('<-5,3,2;-4,2,2>')
    serial_move.print_serial_string()
    
    # Make a undo string as a test
    serial_move = SerialStringUndo()
    serial_move.print_serial_string()
    
    # Make a redo string as a test
    serial_move = SerialStringRedo()
    serial_move.print_serial_string()
    
    # Make a reset string as a test
    serial_move = SerialStringReset()
    serial_move.print_serial_string()

class SerialString:
    def __init__(self):
        self.serial_start_string = '%'
        self.content_start_string = '<'
        self.content_end_string = '>'
    
    def print_serial_string(self):
        print(self.serial_string)
        
class SerialStringBoardState(SerialString):
    def __init__(self, content_string):
        SerialString.__init__(self)
        self.content_string = content_string
        self.type_string = "board_state"
        
        self.serial_string = self.make_serial_string(self.type_string)
        
    def make_serial_string(self, type_string):
        return self.serial_start_string + self.type_string + self.content_string
        
class SerialStringMove(SerialString):
    def __init__(self, content_string):
        SerialString.__init__(self)
        self.content_string = content_string
        self.type_string = "move"
        
        self.serial_string = self.make_serial_string(self.type_string)
    
    def make_serial_string(self, type_string):
        return self.serial_start_string + self.type_string + self.content_string
        
class SerialStringUndo(SerialString):
    def __init__(self):
        SerialString.__init__(self)
        self.type_string = "undo"
        
        self.serial_string = self.make_serial_string(self.type_string)
        
    def make_serial_string(self, type_string):
        return self.serial_start_string + self.type_string
        
class SerialStringRedo(SerialString):
    def __init__(self):
        SerialString.__init__(self)
        self.type_string = "redo"
        
        self.serial_string = self.make_serial_string(self.type_string)
        
    def make_serial_string(self, type_string):
        return self.serial_start_string + self.type_string
        
class SerialStringReset(SerialString):
    def __init__(self):
        SerialString.__init__(self)
        self.type_string = "reset"
        
        self.serial_string = self.make_serial_string(self.type_string)
        
    def make_serial_string(self, type_string):
        return self.serial_start_string + self.type_string

class SerialStringParser(SerialString):
    def __init__(self, serial_string):
        SerialString.__init__(self)
        self.serial_string = serial_string
        
        self.content_string_type, self.content_string = self.parse_serial_string()
        
    def parse_serial_string(self):
        start = self.serial_start_string
        end = self.content_start_string
        string = self.serial_string
        
        content_string_type = string[string.find(start)+len(start):string.rfind(end)]
        
        content_string = string[string.find(self.content_start_string):]
        
        return content_string_type, content_string
    
def read_serial():
    ser = serial.Serial("/dev/ttyACM0", baudrate=9600 ,timeout=1.0)
    ser.flush()
    
    serial_string = ser.read()
    
    if len(serial_string) != 0:
        return SerialStringParser(serial_string)
    else:
        return None
    
if __name__ == "__main__":
    main()