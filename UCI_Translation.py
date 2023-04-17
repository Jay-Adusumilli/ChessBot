from stockfish import Stockfish

class Match:
  def __init__(bot, elo, depth, path, moveTime):
    bot.Pboardstate = [['br1', 'bn1', 'bb1', 'bq', 'bk', 'bb2', 'bn2', 'br2'], #should always be from start on init
                        ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
                        ['wr1', 'wn1', 'wb1', 'wq', 'wk', 'wb2', 'wn2', 'wr2']]
    bot.Cboardstate = bot.Pboardstate
    bot.moveTime = moveTime #2000
    bot.elo = elo #850
    bot.depth = depth #15
    bot.path = path
    stockfish = Stockfish(path=bot.path)
    stockfish.set_elo_rating(bot.elo)
    stockfish.set_depth(bot.depth)

    def displayBoard():
        print(stockfish.get_board_visual())

    def playerMove(boardState):
        bot.Pboardstate = bot.Cboardstate
        bot.Cboardstate = boardState
        from_coords = ['z', 'z']
        to_coords = ['z', 'z']
        cap = False
        illegal = False     
        i = 0
        j = 0
        while i < 8:
            j = 0
            while j < 8:
                if bot.Cboardstate[i][j] != bot.Pboardstate[i][j]:
                    if bot.Cboardstate[i][j] == '-': #All moves
                        moved_from = [i, j] # This will always resolve "moved_from"
                        from_coords[0] = chr(ord('a')+j)
                        from_coords[1] = 8 - i
                    elif bot.Pboardstate[i][j] == '-': #Non-capturing moves
                        moved_to = [i, j] # This will always resolve "moved_to"
                        to_coords[0] = chr(ord('a')+j)
                        to_coords[1] = 8 - i
                        piece = bot.Cboardstate[i][j]
                        cap = False
                    elif bot.Pboardstate[i][j] != '-': # Capturing moves
                        piece = bot.Cboardstate[i][j]
                        piece2 = bot.Pboardstate[i][j]
                        moved_to = [i, j]
                        to_coords[0] = chr(ord('a')+j)
                        to_coords[1] = 8 - i
                        cap = True
                    else:
                        print("Behavior undefined, please reset system.")
                            
                j+=1
            i+=1



        #For Stockfish
        move_input = from_coords[0] + str(from_coords[1]) + to_coords[0] + str(to_coords[1])
        if stockfish.is_move_correct(str(move_input)):
            stockfish.make_moves_from_current_position([move_input])
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
            print('Move is illegal. Please try again.')
        return illegal
    
    def stockfishMove():
        bot.Pboardstate = bot.Cboardstate
        stockfish_move = stockfish.get_best_move_time(bot.moveTime)
        stockfish.make_moves_from_current_position([stockfish_move])
        if (stockfish.will_move_be_a_capture(stockfish_move) == stockfish.Capture.DIRECT_CAPTURE):
            return stockfish_move + 'x'
        elif (stockfish.will_move_be_a_capture(stockfish_move) == stockfish.Capture.EN_PASSANT):
            return stockfish_move + 'x'
        else:
            return stockfish_move