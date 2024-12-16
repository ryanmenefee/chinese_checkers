# -*- coding: utf-8 -*-
"""
Main function for Chinese checkers.

Created on Sun Nov 14 13:40:23 2021

@author: rmene
"""

import game_classes
import serial_classes

def main():
    
    # Initialize game
    game = game_classes.Game()
    game.board.plot_board(show_csys=(True))
    
    # Begin game loop
    while True:
        serial_read = serial_classes.read_serial()
        
        if serial_read.content_string_type == "move":
            move = game_classes.Move(serial_read.content_string)
            game.board.move_piece(move)
            
            game.board.plot_board(show_csys=(True))
                    
if __name__ == "__main__":
    main()