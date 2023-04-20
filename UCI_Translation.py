from stockfish import Stockfish

class Match:
    def __init__(self, elo, depth, moveTime):
        #Match.Pboardstate = [['br1', 'bn1', 'bb1', 'bq', 'bk', 'bb2', 'bn2', 'br2'], #should always be from start on init
        #                    ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'], 
        #                    ['-', '-', '-', '-', '-', '-', '-', '-'], 
        #                    ['-', '-', '-', '-', '-', '-', '-', '-'], 
        #                    ['-', '-', '-', '-', '-', '-', '-', '-'], 
        #                    ['-', '-', '-', '-', '-', '-', '-', '-'], 
        #                    ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
        #                    ['wr1', 'wn1', 'wb1', 'wq', 'wk', 'wb2', 'wn2', 'wr2']]
        Match.Pboardstate = [['-', '-', '-', 'wq', 'wk', '-', '-', '-'], #should always be from start on init
                            ['-', '-', 'wp', 'wp', 'wp', 'wp', '-', '-'], 
                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                            ['-', '-', 'bp', 'bp', 'bp', 'bp', '-', '-'],
                            ['-', '-', '-', 'bq', 'bk', '-', '-', '-']]
        
        Match.Cboardstate = Match.Pboardstate
        Match.moveTime = moveTime #2000
        Match.elo = elo #850
        Match.depth = depth #15
        #Match.path = r"C:\Users\Jay\Documents\_Clemson\Senior Design\stockfish_15.1_win_x64_avx2"
        #stockfish = Stockfish(path=Match.path)
        Match.stockfish = Stockfish(path=r"C:\Users\Jay\Documents\_Clemson\SeniorDesign\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2")
        Match.stockfish.set_elo_rating(Match.elo)
        Match.stockfish.set_depth(Match.depth)
        Match.stockfish.set_fen_position('3qk3/2pppp2/8/8/8/8/2PPPP2/3QK3 w - - 0 0')

    def setPboardstate(self, boardState):
        Match.Pboardstate = boardState

    def displayBoard(self):
        print(Match.stockfish.get_board_visual())

    def playerMove(self, boardState):
        Match.Pboardstate = Match.Cboardstate
        Match.Cboardstate = boardState
        from_coords = ['z', 'z']
        to_coords = ['z', 'z']
        cap = False
        illegal = False     
        i = 0
        j = 0
        while i < 8:
            j = 0
            while j < 8:
                if Match.Cboardstate[i][j] != Match.Pboardstate[i][j]:
                    if Match.Cboardstate[i][j] == '-': #All moves
                        from_coords[0] = chr(ord('a')+j)
                        from_coords[1] = 1 + i
                    elif Match.Pboardstate[i][j] == '-': #Non-capturing moves
                        to_coords[0] = chr(ord('a')+j)
                        to_coords[1] = 1 + i
                        piece = Match.Cboardstate[i][j]
                        cap = False
                    elif Match.Pboardstate[i][j] != '-': # Capturing moves
                        piece = Match.Cboardstate[i][j]
                        piece2 = Match.Pboardstate[i][j]
                        to_coords[0] = chr(ord('a')+j)
                        to_coords[1] = 1 + i
                        cap = True
                    else:
                        print("Behavior undefined, please reset system.")
                            
                j+=1
            i+=1

        #For Stockfish
        move_input = from_coords[0] + str(from_coords[1]) + to_coords[0] + str(to_coords[1])
        print("Move input: ", move_input)
        if Match.stockfish.is_move_correct(str(move_input)):
            Match.stockfish.make_moves_from_current_position([move_input])
            illegal = False
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
        else:
            illegal = True
            print(move_input)
        return illegal
    
    def stockfishMove(self):
        Match.Pboardstate = Match.Cboardstate
        stockfish_move = Match.stockfish.get_best_move_time(Match.moveTime)
        print("stockfish move ", stockfish_move)
        print(Match.stockfish.will_move_be_a_capture(stockfish_move))
        Match.stockfish.make_moves_from_current_position([stockfish_move])
        return stockfish_move
        if (Match.stockfish.will_move_be_a_capture(str(stockfish_move)) == Stockfish.Capture.DIRECT_CAPTURE):
            return stockfish_move + 'x'
        elif (Match.stockfish.will_move_be_a_capture(str(stockfish_move)) == Stockfish.Capture.EN_PASSANT):
            return stockfish_move + 'x'
        else:
            return stockfish_move
        

match = Match(850, 15, 2000)
print("Before player move")
match.displayBoard()
vision_board = [['-', '-', '-', 'wq', 'wk', '-', '-', '-'],
                ['-', '-', 'wp', 'wp', 'wp', '-', '-', '-'],
                ['-', '-', '-', '-', '-', 'wp', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', 'bp', 'bp', 'bp', 'bp', '-', '-'],
                ['-', '-', '-', 'bq', 'bk', '-', '-', '-']]
match.playerMove(vision_board)
print("After player move")
match.displayBoard()
match.stockfishMove()
print("After stockfish move")
match.displayBoard()

vision_board = [['-', '-', '-', 'wq', 'wk', '-', '-', '-'],
                ['-', '-', '-', 'wp', 'wp', '-', '-', '-'],
                ['-', '-', 'wp', '-', '-', 'wp', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', 'bp', 'bp', 'bp', 'bp', '-', '-'],
                ['-', 'bq', '-', '-', 'bk', '-', '-', '-']]


match.playerMove(vision_board)
print("After player move")
match.displayBoard()
match.stockfishMove()
print("After stockfish move")
match.displayBoard()
