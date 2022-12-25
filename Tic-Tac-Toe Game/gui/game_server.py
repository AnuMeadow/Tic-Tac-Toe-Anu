import socket
import threading

PORT = 10000
IP = '127.0.0.1'


'''
index is as follows:


       |       |        
    0  |   1   |   2    
_______|_______|________
       |       |        
    3  |   4   |   5    
_______|_______|________            
       |       |
    6  |   7   |   8
       |       |        



'''

game_grid = ['' for i in range(9)]
group_list = [[0,1,2],
              [3,4,5],
              [6,7,8],
              [0,3,6],
              [1,4,7],
              [2,5,8],
              [0,4,8],
              [2,4,6]]


'''
first person will get X as symbol
second person will get O as symbol
player1---->X
player2---->O

if any player quits abruptly, then we will stop server and 
close all connections

the game server will communicate with players using 5 kind of messages:
1. ACT: to denote that this is that player's turn and ask
for the position it places X or O
2. POS: to denote the other player has finished his turn
by picking a position and this player must update its board
3. ERR: to denote an error or an abrupt closure of connection by other/all players.
4. RES: result of the game.
5. INI: initial welcome and setup message to player
'''
game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
game_server.bind((IP, PORT))
print('[CREATED SERVER]')

players_in = 0
players_list = []

class Player:
    def __init__(self, conn, addr, symbol):
        self.conn = conn
        self.addr = addr
        #can be either X or O
        self.symbol = symbol



def listen_connection():
    global players_in
    global players_list

    print('[WAITING FOR PLAYERS]......')
    game_server.listen()
    print('[LISTENING] Server is listening....')

    while players_in<2:
        conn, addr = game_server.accept()        
        players_in +=1
        print(f'[CONNECTED] to {addr}')

        if players_in == 1:
            player = Player(conn, addr, 'X')
            conn.sendall('INI:Welcome player. Your symbol is X'.encode())
        else:
            player = Player(conn, addr, 'O')
            conn.sendall('INI:Welcome player. Your symbol is O'.encode())
        players_list.append(player)
    print('[PLAYERS JOINED]')



def check_win(index):
    won = False
    win_char = ''

    for group in group_list:
        if index in group:

            character = game_grid[index]

            if game_grid[group[0]] == game_grid[group[1]] and\
                game_grid[group[0]] == game_grid[group[2]]:
                
                win_char = character
                won = True
                break
    
    return (won, win_char)



def check_draw():

    draw = True
    if '' in game_grid:
        draw = False

    return draw
 


def evaluate(index):
    # return break_out_of_while_loop:bool, character_won:string
    res = check_win(index)
    if res[0]:
        return True, 1 if res[1]=='O' else 0
    elif check_draw():
        return (True, '')
    else:
        return (False, '')



def close_connections():

    if len(players_list)<2:
        print('[ERROR OCCURRED] Client/s abruptly ended connection')

        if len(players_list) == 1:
            players_list[0].conn.sendall('ERR:Other Player ended connection.'.encode())
            players_list[0].conn.close()
    else:
        for player in players_list:
            print(f'[CONNECTION CLOSED] to {player.addr}')
            player.conn.close()



def play():

    turn =0

    while True:
        try:
            players_list[turn].conn.sendall('ACT:Your Turn. Choose a index'.encode())
            ## index returns a int
            index = players_list[turn].conn.recv(1024).decode()
            # need to send position to other player,
            # so they can change their board accordingly
            players_list[(turn+1)%2].conn.sendall(('POS:'+index).encode())

            index = int(index)
            game_grid[index] = players_list[turn].symbol
            ## returns True if Draw or win occured
            ## winner can be '' if Draw or an index in (0,1) depending upon who won
            breakout_of_loop, winner = evaluate(index)

            if breakout_of_loop:
                ## sending win/draw messages

                if winner == '':        #Draw occured
                    for player in players_list:
                        player.conn.sendall('RES:Draw'.encode())
                else:
                    #print(winner)
                    players_list[winner].conn.sendall('RES:You Won'.encode())
                    players_list[(winner+1)%2].conn.sendall('RES:You Lost'.encode())                
                
                break
        except Exception as e:
            print(e)
            print('[ERROR OCCURED] Closing Application......')
            players_list.remove(players_list[turn])
            break
        finally:
            turn = (turn+1)%2    
            
listen_connection()
play()
close_connections()
print('[CLOSING SERVER] Bye....')
game_server.close()
