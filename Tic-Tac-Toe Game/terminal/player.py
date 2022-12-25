import socket

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

game_grid = [' ' for i in range(9)]


'''
the game server will communicate with players using 5 kind of messages:
1. ACT: to denote that this is that player's turn and ask
for the position it places X or O
2. POS: to denote the other player has finished his turn
by picking a position and this player must update its board
3. ERR: to denote an error or an abrupt closure of connection by other/all players.
4. RES: result of the game.
5. INI: initial welcome and setup message to player
'''

def display_grid():

    print()
    print('==============================GRID=======================')
    print()
    print('         |         |')
    print(f'    {game_grid[0]}    |    {game_grid[1]}    |    {game_grid[2]}')
    print('         |         |')
    print('_________|_________|_________')
    print('         |         |')
    print(f'    {game_grid[3]}    |    {game_grid[4]}    |    {game_grid[5]}')
    print('         |         |')
    print('_________|_________|_________')
    print('         |         |')
    print(f'    {game_grid[6]}    |    {game_grid[7]}    |    {game_grid[8]}')
    print('         |         |')



## print the index to grid mapping
print('The index to position mapping is as follows:')
print('\t0|1|2\n\t3|4|5\n\t6|7|8\n')
        

player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player.connect((IP, PORT))
player_symbol = ''
print('[CONNECTING TO SERVER].....')


while True:
    data = player.recv(1024).decode()
    if data[:3] == 'INI':
        ## last character will be the symbol for this player
        player_symbol = data[-1:]
        print('[SERVER] '+data[4:])
    elif data[:3] == 'ACT':
        print('[SERVER] '+data[4:])
        
        
        while True:
            index = input('You>>>')
            
            if not index.isdigit() or game_grid[int(index)] != ' ':
                print('Position already filled, Choose another.')
            else:
                break
        
        #print('hey',type(index),index)
        game_grid[int(index)] = player_symbol
        display_grid()
        player.sendall(index.encode())

    elif data[:3] == 'POS':
        index = int(data[4:])
        game_grid[index] = 'O' if player_symbol =='X' else 'X'
        display_grid()
    
    elif data[:3] == 'ERR':

        print('[SERVER] '+data[4:])
        print('[CLOSING CONNECTION TO SERVER]....')
        print('Exiting Game....')
        player.close()
        break
    elif data[:3] == 'RES':

        print('[SERVER] '+data[4:])
        print('[CLOSING CONNECTION]....')
        print('Exiting Game....')
        player.close()
        break
