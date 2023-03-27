moved_from = [-1, -1]
from_coords = ['z', 'z']
moved_to = [-1, -1]
to_coords = ['z', 'z']
cap = False
move_input = ''
temp_board = [['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],]
prev_board = [['br1', 'bn1', 'bb1', 'bq', 'bk', 'bb2', 'bn2', 'br2'], 
              ['bp1', 'bp2', '-', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'], 
              ['-', '-', '-', '-', '-', '-', '-', '-'], 
              ['-', '-', '-', '-', '-', '-', '-', '-'], 
              ['-', '-', '-', '-', '-', '-', '-', '-'], 
              ['-', '-', 'bp3', '-', '-', '-', '-', '-'], 
              ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
              ['wr1', 'wn1', 'wb1', 'wq', 'wk', 'wb2', 'wn2', 'wr2']]
curr_board = [['br1', 'bn1', 'bb1', 'bq', 'bk', 'bb2', 'bn2', 'br2'], 
              ['bp1', 'bp2', '-', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'], 
              ['-', '-', '-', '-', '-', '-', '-', '-'], 
              ['-', '-', '-', '-', '-', '-', '-', '-'], 
              ['-', '-', '-', '-', '-', '-', '-', '-'], 
              ['-', '-', 'wp2', '-', '-', '-', '-', '-'], 
              ['wp1', '-', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
              ['wr1', 'wn1', 'wb1', 'wq', 'wk', 'wb2', 'wn2', 'wr2']]
#while(True)
             
i = 0
j = 0
while i < 8:
    j = 0
    while j < 8:
        if curr_board[i][j] != prev_board[i][j]:
            if curr_board[i][j] == '-': #All moves
                moved_from = [i, j] # This will always resolve "moved_from"
                from_coords[0] = chr(ord('a')+j)
                from_coords[1] = 8 - i
            elif prev_board[i][j] == '-': #Non-capturing moves
                moved_to = [i, j] # This will always resolve "moved_to"
                to_coords[0] = chr(ord('a')+j)
                to_coords[1] = 8 - i
                piece = curr_board[i][j]
                cap = False
            elif prev_board[i][j] != '-': # Capturing moves
                piece = curr_board[i][j]
                piece2 = prev_board[i][j]
                moved_to = [i, j]
                to_coords[0] = chr(ord('a')+j)
                to_coords[1] = 8 - i
                cap = True
            else:
                print("Behavior undefined, please reset system.")
                    
        j+=1
    i+=1

if cap:
    print('{0} from'.format(piece), end = ' ')
    print(*from_coords, sep='', end = ' ')
    print('captured {0} at'.format(piece2), end = ' ')
    print(*to_coords, sep='')
else:
    print('Moved {0} from'.format(piece), end = ' ')
    print(*from_coords, sep='', end = ' ')
    print('to', end = ' ')
    print(*to_coords, sep='')

#For Stockfish
move_input = from_coords[0] + str(from_coords[1]) + to_coords[0] + str(to_coords[1])
#reset all vars down here and update board states