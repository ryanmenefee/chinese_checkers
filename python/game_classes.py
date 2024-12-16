# -*- coding: utf-8 -*-
"""
Defines class objects for game logic.

Created on Sun Nov 14 13:40:23 2021

@author: rmene
"""

import math
import matplotlib.pyplot as plt

def main():
    # Testing of various game actions
    
    game = Game()
    
    game.board.plot_board(show_csys=(True))
    
    remote_game = Game()
    board_compare = game.board.compare_board_states(game.board.state, remote_game.board.state)
    print(board_compare)
    
    move = Move(start_coord=[5,-3,-2], end_coord=[4,-2,-2])
    game.board.move_piece(move)
    game.board.plot_board(show_csys=(True))
    
    move = Move(start_coord=[-5,3,2], end_coord=[-4,2,2])
    game.board.move_piece(move)
    move.print_move()
    game.board.plot_board(show_csys=(True))
    
    game.board.undo_move()
    move_string = move.make_move_string()
    print(move_string)
    move = Move(move_string=move_string)
    move.print_move()
    game.board.move_piece(move)
    game.board.plot_board(show_csys=(True))
    
    # move = Move(start_coord=[5,-3,-2], end_coord=[0,0,0])
    # game.board.move_piece(move)
    # game.board.plot_board(show_csys=(True))
    
    # remote_game = Game()
    # board_compare = game.board.compare_board_states(game.board.state, remote_game.board.state)
    # print(board_compare)
    
    board_state_string = game.board.make_board_state_string()
    print(board_state_string)
    
    # board_state_read_from_string = game.board.read_board_state(board_state_string)
    
    # print('\n' + 30 * '*')
    # print('Move History 1:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 1:')
    # game.board.move_cache.print_move_future()
    
    # game.board.undo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 2:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 2:')
    # game.board.move_cache.print_move_future()
    
    # game.board.redo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 3:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 3:')
    # game.board.move_cache.print_move_future()
    
    # game.board.undo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 4:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 4:')
    # game.board.move_cache.print_move_future()
    
    # game.board.undo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 5:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 5:')
    # game.board.move_cache.print_move_future()
    
    # move = Move(start_coord=[5,-2,-3], end_coord=[4,-1,-3])
    # game.board.move_piece(move)
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 6:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 6:')
    # game.board.move_cache.print_move_future()
    
    # game.board.redo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 7:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 7:')
    # game.board.move_cache.print_move_future()
    
    # game.board.undo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 8:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 8:')
    # game.board.move_cache.print_move_future()
    
    # game.board.undo_move()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 9:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 9:')
    # game.board.move_cache.print_move_future()
    
    # move = Move(start_coord=[5,-3,-2], end_coord=[4,-2,-2])
    # game.board.move_piece(move)
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 10:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 10:')
    # game.board.move_cache.print_move_future()
    
    # game.board.reset()
    # game.board.plot_board(show_csys=(True))
    
    # print('\n' + 30 * '*')
    # print('Move History 11:')
    # game.board.move_cache.print_move_history()
    
    # print('\nMove Future 11:')
    # game.board.move_cache.print_move_future()
    
class Game:
    def __init__(self):
        self.board = Board()
    
class Board:
    def __init__(self):
        self.board_size = 4
        self.player_id_map = [0, 1, 2, 3, 4, 5, 6]
        self.player_color_map = ['none', 'r', 'g', 'b', 'm', 'y', 'c']
        self.communication_start_string = '<'
        self.communication_end_string = '>'
        self.communication_minor_delimiter = ','
        self.communication_major_delimiter = ';'
        
        self.radius = (2 * self.board_size) + 1
        self.bounding_line = self.board_size
        self.state = self.init_board_state()
        self.move_cache = MoveCache()
        
    def reset(self):
        self.state = self.init_board_state()
        self.move_cache = MoveCache()
        
    def move_piece(self, move, should_save=True, should_erase_future_cache=True):
        # Verify start coordinate is on the board. Do not move the piece if
        # it is not.
        coord_on_board = self.check_if_coord_on_board(move.start_coord)
        if not coord_on_board:
            print('Start coordinate is not on the board.')
            return
        
        # Verify end coordinate is on the board. Do not move the piece if
        # it is not.
        coord_on_board = self.check_if_coord_on_board(move.end_coord)
        if not coord_on_board:
            print('End coordinate is not on the board.')
            return
        
        # Verify a player piece is at the start coordinate
        if self.get_player_id_at_coord(move.start_coord) == 0:
            print('No piece located at the start coordinate.')
            return 
        
        # Verify the end coordinate is empty
        if not self.get_player_id_at_coord(move.end_coord) == 0:
            print('Another piece is already located at the end coordinate.')
            return 
        
        # Get index of start and end coordinates
        for ii, location in enumerate(self.state):
            if location.coord == move.start_coord:
                start_index = ii
            elif location.coord == move.end_coord:
                end_index = ii
                
        # Swap start and end coordinates
        self.state[start_index].coord = move.end_coord
        self.state[end_index].coord = move.start_coord
        
        # Store move in move history
        if should_save:
            self.move_cache.save_move(move)
            
        # Erase future move cache
        if should_erase_future_cache:
            self.move_cache.erase_future()
        
    def check_if_coord_on_board(self, coord):
        if sum(coord) != 0:
            return False
        
        for x in coord:
            if abs(x) >= self.radius:
                return False
            
        return True
    
    def get_player_id_at_coord(self, coord):
        for location in self.state:
            if location.coord == coord:
                player_id = location.player_id
        
        return player_id

    def undo_move(self):
        if self.move_cache.get_last_move() == None:
            print('Cannot undo, no previous move.')
            return
        
        move_undo = self.move_cache.get_last_move().get_reverse_move()
        self.move_piece(move_undo, should_save=False, should_erase_future_cache=False)
        
        self.move_cache.traverse_backwards()
        
    def redo_move(self):
        if self.move_cache.get_next_move() == None:
            print('Cannot redo, no undone move.')
            return
        
        move_redo = self.move_cache.get_next_move()
        self.move_piece(move_redo, should_save=False, should_erase_future_cache=False)
        
        self.move_cache.traverse_forwards()
        
    def make_board_state_string(self):
        board_state_list = [self.communication_start_string]
        
        for location in self.state:
            format_string = '{coord0}{minor_delimiter}{coord1}{minor_delimiter}{coord2}{minor_delimiter}{player_id}{major_delimiter}'
            data_string = format_string.format( \
                                              coord0 = location.coord[0], \
                                              coord1 = location.coord[1], \
                                              coord2 = location.coord[2], \
                                              player_id = location.player_id, \
                                              minor_delimiter = self.communication_minor_delimiter, \
                                              major_delimiter = self.communication_major_delimiter \
                                                  )
            board_state_list.append(data_string)
        
        # Strip the extra location delimiter
        board_state_list[-1] = board_state_list[-1][0:-1]
        
        board_state_list.append(self.communication_end_string)
        
        board_state_string = ''.join(board_state_list)
        
        return board_state_string
    
    def read_board_state(self, board_state_string):
        # Strip start and end strings
        board_state_string = board_state_string.lstrip(self.communication_start_string)
        board_state_string = board_state_string.rstrip(self.communication_end_string)
        
        # Split string into list of location data (coordinates and player IDs)
        board_state_list = board_state_string.split(self.communication_major_delimiter)
        
        # Populate board state by splitting location data into coordinates and
        # player IDs
        board_state = []
        for location_string in board_state_list:
            data = location_string.split(self.communication_minor_delimiter)
            coord = data[0:3]
            player_id = data[3]
            
            location = Location(coord, player_id)
            
            board_state.append(location)
            
        return board_state
        
    def compare_board_states(self, board_state_1, board_state_2):
        """
        Compares board states.

        Parameters
        ----------
        board_state_1 : List of location objects
            First board state to compare.
        board_state_2 : List of location objects
            Second board state to compare.

        Returns
        -------
        board_state_comparison : Boolean
            Returns true if the input board states are identical and false
            otherwise.

        """
        # Assume board states are the same 
        board_state_comparison = True
        
        # Begin looping through every location in the board and compare the two
        # states. Return false on the first location result that is not 
        # identical.
        for location_1 in board_state_1:
            index = self.find_location_in_state(board_state_2, location_1)
            
            if location_1.player_id != board_state_2[index].player_id:
                board_state_comparison = False
                break
        
        return board_state_comparison
    
    def find_location_in_state(self, state, location_to_find):
        index = [ii for ii, x in enumerate(state) if x.coord == location_to_find.coord][0]
        
        return index
    
    def update_board_state(self, new_board_state):
        self.state = new_board_state
        
    def plot_board(self, show_csys):
        """
        Plots the board state

        Returns
        -------
        None.

        """
        # Get the coordinates of the board
        tri_coord = []
        for location in self.state:
            tri_coord.append(location.coord)
        
        # Get plot limits
        cart_coord = []
        for coord in tri_coord:
            cart_coord.append(self.triangular_to_cartesian(coord))
        
        x = [a[0] for a in cart_coord]
        y = [a[1] for a in cart_coord]
        max_x = max([abs(a) for a in x])
        max_y = max([abs(a) for a in y])
        limit = max(max_x, max_y) * 1.3
        
        # Create plot
        fig, ax = plt.subplots(1)
        plt.xlim(-limit, limit)
        plt.ylim(-limit, limit)
        ax.set_aspect('equal', adjustable='box')
        for location in self.state:
            # Get cartesion coordinates of location
            cart_coord = self.triangular_to_cartesian(location.coord)
            
            # Get color corresponding to player
            color = self.get_player_color(location.player_id)
            
            plt.scatter(cart_coord[0], cart_coord[1], facecolors=color, edgecolors='k')
        
        # Plot the coordinate system
        if show_csys:
            arrow_radius = 1.55
            annotation_radius = arrow_radius * 1.0
            arrow_transparency = 0.3
            annotation_transparency = 0.3
            
            arrow_coords      = self.triangular_to_cartesian([self.radius * arrow_radius, 0, 0])
            annotation_coords = self.triangular_to_cartesian([self.radius * annotation_radius, 0, 0])
            ax.annotate("",  xy=(arrow_coords[0], arrow_coords[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", alpha=arrow_transparency))
            ax.annotate("A", xy=(annotation_coords[0], annotation_coords[1]), alpha = annotation_transparency)
            
            arrow_coords      = self.triangular_to_cartesian([0, self.radius * arrow_radius, 0])
            annotation_coords = self.triangular_to_cartesian([0, self.radius * annotation_radius, 0])
            ax.annotate("",  xy=(arrow_coords[0], arrow_coords[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", alpha=arrow_transparency))
            ax.annotate("B", xy=(annotation_coords[0], annotation_coords[1]), alpha = annotation_transparency)
            
            arrow_coords      = self.triangular_to_cartesian([0, 0, self.radius * arrow_radius])
            annotation_coords = self.triangular_to_cartesian([0, 0, self.radius * annotation_radius * 1.07])
            ax.annotate("",  xy=(arrow_coords[0], arrow_coords[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", alpha=arrow_transparency))
            ax.annotate("C", xy=(annotation_coords[0], annotation_coords[1]), alpha = annotation_transparency)   
        
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        
        # Show the plot
        plt.show()
    
    def get_player_color(self, player_id):
        """
        Get color string from player ID

        Parameters
        ----------
        player_id : integer
            Player ID integer.

        Returns
        -------
        color : string
            Matplotlib color format string.

        """
        
        color = self.player_color_map[player_id]
        
        return color
    
    def init_board_state(self):
        # Initial board state variable
        state = []
        
        # Get list of triangular coordinates
        coords = self.init_board_coord()
        
        # For each coordinate, assign a player ID by checking to see if the 
        # coordinates of a piece are outside bounding lines
        for coord in coords:
            if coord[0]>self.bounding_line:
                player_id = 1
            elif coord[1]>self.bounding_line:
                player_id = 2
            elif coord[2]>self.bounding_line:
                player_id = 3
            elif -coord[0]>self.bounding_line:
                player_id = 4
            elif -coord[1]>self.bounding_line:
                player_id = 5
            elif -coord[2]>self.bounding_line:
                player_id = 6
            else:
                player_id = 0
            
            state.append(Location(coord, player_id))
        
        return state
    
    def init_board_coord(self):
        """
        Makes triangular coordinates of all board piece locations
    
        Returns
        -------
        board_coord : list
            List of lists of 3 triangular coordinates [[a1,b1,c1], end_coord=[a2,b2,c2], ...]
    
        """
        
        board_coord = []
        
        # Get hexgonal grid
        deltas = [[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]]
        for r in range(self.radius):
            a = 0
            b = -r
            c = +r
            board_coord.append([a,b,c])
            for ii in range(6):
                if ii==5:
                    num_of_hexas_in_edge = r-1
                else:
                    num_of_hexas_in_edge = r
                for jj in range(num_of_hexas_in_edge):
                    a = a+deltas[ii][0]
                    b = b+deltas[ii][1]
                    c = c+deltas[ii][2]            
                    board_coord.append([a,b,c])
        
        # Trim points from hexagonal grid that lie outside possible piece
        # locations (Outside 6 pointed star)
        coord_to_trim = []
        for coord in board_coord:
            num_outside_bounding_lines = sum([
                                             coord[0]>self.bounding_line,
                                             coord[1]>self.bounding_line,
                                             coord[2]>self.bounding_line,
                                            -coord[0]>self.bounding_line,
                                            -coord[1]>self.bounding_line,
                                            -coord[2]>self.bounding_line,
                                            ])
            
            if num_outside_bounding_lines > 1:
                coord_to_trim.append(coord)
                
        for coord in coord_to_trim:
            board_coord.remove(coord)
                    
        return board_coord
    
    def triangular_to_cartesian(self, tri_coord):
        """
        Convert triangular coordinates to Cartesian
        
        Parameters
        ----------
        tri_coord : list
            3 triangular coordinates [a,b,c]
    
        Returns
        -------
        cart_coord : list
            2 Cartesian coordinates [x, y]
    
        """
        a = tri_coord[0]
        b = tri_coord[1]
        c = tri_coord[2]
               
        x =  b*math.cos(math.radians(30)) - c*math.cos(math.radians(30))
        y = -b*math.cos(math.radians(60)) - c*math.cos(math.radians(60)) + a
        
        cart_coord = [x, y]
        
        return cart_coord
    
class Location:
    def __init__(self, coord, player_id):
        self.coord     = coord
        self.player_id = player_id
        
class Move:
    def __init__(self, **kwargs):
        self.communication_start_string = '<'
        self.communication_end_string = '>'
        self.communication_minor_delimiter = ','
        self.communication_major_delimiter = ';'
        
        self.start_coord = kwargs.get('start_coord')
        self.end_coord   = kwargs.get('end_coord')
        
        if kwargs.get('move_string') != None:
            self.start_coord, self.end_coord = self.read_move_string(kwargs.get('move_string'))
        
    def make_move_string(self):
        format_string = '{communication_start_string}' + \
                        '{start_coord0}{minor_delimiter}{start_coord1}{minor_delimiter}{start_coord2}' + \
                        '{major_delimiter}' + \
                        '{end_coord0}{minor_delimiter}{end_coord1}{minor_delimiter}{end_coord2}' + \
                        '{communication_end_string}'
        move_string = format_string.format( \
                                          communication_start_string = self.communication_start_string, \
                                          communication_end_string = self.communication_end_string, \
                                          start_coord0 = self.start_coord[0], \
                                          start_coord1 = self.start_coord[1], \
                                          start_coord2 = self.start_coord[2], \
                                          end_coord0 = self.end_coord[0], \
                                          end_coord1 = self.end_coord[1], \
                                          end_coord2 = self.end_coord[2], \
                                          minor_delimiter = self.communication_minor_delimiter, \
                                          major_delimiter = self.communication_major_delimiter \
                                              )
        
        return move_string
        
    def read_move_string(self, move_string):
        # Strip start and end strings
        move_string = move_string.lstrip(self.communication_start_string)
        move_string = move_string.rstrip(self.communication_end_string)
        
        # Split string into coordinate strings
        start_coord_string, end_coord_string = move_string.split(self.communication_major_delimiter)
        
        # Convert coordinate strings to coordinate list
        start_coord = [int(x) for x in start_coord_string.split(self.communication_minor_delimiter)]
        end_coord = [int(x) for x in end_coord_string.split(self.communication_minor_delimiter)]
            
        return start_coord, end_coord
        
    def get_reverse_move(self):
        return Move(start_coord=self.end_coord, end_coord=self.start_coord)      
        
    def print_move(self):
        print('\nStart Coord: ', self.start_coord)
        print('End Coord: ',   self.end_coord)
        
class MoveCache:
    def __init__(self):
        self.move_history = []
        self.move_future  = []
        
    def save_move(self, move):
        self.move_history.append(move)
        
    def get_last_move(self):
        if len(self.move_history) == 0:
            return None
        
        return self.move_history[-1]
    
    def get_next_move(self):
        if len(self.move_future) == 0:
            return None
        
        return self.move_future[0]
        
    def print_move_history(self):
        for move in self.move_history:
            print(move.start_coord, move.end_coord)
            
    def print_move_future(self):
        for move in self.move_future:
            print(move.start_coord, move.end_coord)
            
    def traverse_backwards(self):
        self.move_future.insert(0, self.move_history.pop())
        
    def traverse_forwards(self):
        self.move_history.append(self.move_future.pop(0))
        
    def erase_future(self):
        self.move_future = []
                    
if __name__ == "__main__":
    main()