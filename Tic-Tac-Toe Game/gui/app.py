import tkinter as tk
import socket
import threading
from PIL import ImageTk, Image

Font_tuple1 = ("Comic Sans MS", 20, "bold")
Font_tuple2 = ("Comic Sans MS", 13)

class CustomLabel(tk.Label):

    def __init__(self,index, **args):
        tk.Label.__init__(self, **args)
        self.index = index

class Gui:

    def __init__(self):
        self.game_grid = [' ' for i in range(9)]
        self.window = tk.Tk()
        self.window.title('Tic tac toe Game')
        self.window.config(bg='#00ddb0')
        self.window.geometry('600x700')
        self.window.resizable(False, False)
        
        self.label_List = []
        self.symbol_image=None

        for i in range(9):
            label = CustomLabel(i,bg='#00ddb0', width=200, height=200, relief='groove', borderwidth=4)
            self.label_List.append(label)
            label.place(x=(i%3)*200, y=(i//3)*200)

        self.labelFooter = tk.Label(bg='#210070', width=600, height=200, relief='groove', borderwidth=4)
        self.labelFooter.place(x=0, y=600)

        self.result_label = tk.Label(text= 'hello',font=Font_tuple2,bg='#210070', fg='#00ddb0')
        self.result_label.place(x=280, y=640)

        symbol_thread = threading.Thread(target=self.get_input)
        symbol_thread.start()
        self.window.mainloop()


    def get_input(self):

        symbol = input('>>Enter symbol(X,O):')

        if symbol.upper()=='X':
            self.symbol_image = self.get_img('./pics/cross.png')
        else:
            self.symbol_image = self.get_img('./pics/nought.png')

        for i in range(9):
            self.label_List[i].bind('<Button-1>', self.display_img)

    def get_img(self,img_path):
        img = Image.open(img_path)
        resized_img = img.resize((200,200), Image.ANTIALIAS)
        res_img = ImageTk.PhotoImage(resized_img)

        return res_img


    def display_img(self, event):
        widget = event.widget
        widget.config(image=self.symbol_image)
        print(widget.index)


gui= Gui()