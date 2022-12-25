import tkinter as tk
import socket
import threading
from PIL import ImageTk, Image

PORT = 10000
IP = '127.0.0.1'

Font_tuple1 = ("Comic Sans MS", 20, "bold")
Font_tuple2 = ("Comic Sans MS", 13)

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

class CustomLabel(tk.Label):

    def __init__(self,index, **args):
        tk.Label.__init__(self, **args)
        self.index = index


class Gui:

    def __init__(self):
        self.game_grid = [' ' for i in range(9)]
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe Game')
        self.window.config(bg='#00ddb0')
        self.window.geometry('600x750')
        self.window.resizable(False, False)

        self.label_List = []
        self.symbol_image=None
        self.symbol = None
        self.index_chosen = None

        for i in range(9):
            label = CustomLabel(i,bg='#00ddb0', width=200, height=200, relief='groove', borderwidth=4)
            self.label_List.append(label)
            label.place(x=(i%3)*200, y=(i//3)*200)

        self.labelFooter = tk.Label(bg='#210070', width=600, height=200, relief='groove', borderwidth=4)
        self.labelFooter.place(x=0, y=600)

        self.turn_label = tk.Label(text='', font=Font_tuple2,bg='#210070', fg='#00ddb0')
        self.turn_label.place(x=280, y=640)
        self.result_label = tk.Label(text= '',font=Font_tuple2,bg='#210070', fg='#00ddb0')
        self.result_label.place(x=280, y=670)

        self.nought_img = self.get_img('./pics/nought.png')
        self.cross_img = self.get_img('./pics/cross.png')

        self.player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player.connect((IP, PORT))

        self.start_game()
        self.window.mainloop()
    

    def enable_click(self):
        for i in range(9):
            self.label_List[i].bind('<Button-1>', self.choose_this_label)

    def disable_click(self):
        for i in range(9):
            self.label_List[i].unbind('<Button-1>')


    def get_img(self,img_path):
        img = Image.open(img_path)
        resized_img = img.resize((200,200), Image.ANTIALIAS)
        res_img = ImageTk.PhotoImage(resized_img)

        return res_img

    def choose_this_label(self, event):
        widget = event.widget
        self.index_chosen = widget.index

    def display_img(self, index, img):        
        self.label_List[index].config(image=img)
        
    def start_game(self):      
        player_thread = threading.Thread(target=self.handle_connection)
        player_thread.start()

    def handle_connection(self):
        while True:
            data = self.player.recv(1024).decode()
            if data[:3] == 'INI':
                ## last character will be the symbol for this player
                if data[-1:]=='X':
                    self.symbol_image = self.cross_img
                    self.symbol = 'X'
                else:
                    self.symbol_image = self.nought_img
                    self.symbol = 'O'

            elif data[:3] == 'ACT':
                print('[SERVER] '+data[4:])
                self.turn_label.config(text='your turn')
                self.enable_click()
                
                while True:
                    
                    while True:
                        if self.index_chosen != None:
                            break
                    
                    print(self.index_chosen)

                    if self.game_grid[self.index_chosen] == ' ':
                        self.display_img(self.index_chosen, self.symbol_image)
                        self.game_grid[self.index_chosen]=self.symbol
                        break
                
                #print('hey',type(index),index)
                
                self.player.sendall(str(self.index_chosen).encode())
                self.disable_click()
                self.index_chosen = None
                self.turn_label.config(text="opponent's turn")

            elif data[:3] == 'POS':
                index = int(data[4:])
                self.game_grid[index] = 'O' if self.symbol =='X' else 'X'
                opponent_img = self.nought_img if self.symbol =='X' else self.cross_img
                self.display_img(index, opponent_img)
            
            elif data[:3] == 'ERR':

                print('[SERVER] '+data[4:])
                print('[CLOSING CONNECTION TO SERVER]....')
                print('Exiting Game....')
                self.result_label.config(text=data[4:])
                self.turn_label.config(text='')
                self.player.close()
                break
            elif data[:3] == 'RES':

                print('[SERVER] '+data[4:])
                print('[CLOSING CONNECTION]....')
                print('Exiting Game....')
                self.result_label.config(text=data[4:])
                self.turn_label.config(text='')
                self.player.close()
                break




gui= Gui()