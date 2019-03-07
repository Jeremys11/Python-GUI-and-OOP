from RandomEvent import *
from Battle import *
from tkinter import messagebox


class GameBoard(Frame):
    def __init__(self):
        self.board = Tk()
        Frame.__init__(self, self.board)
        self.board.protocol("WM_DELETE_WINDOW", self.on_exit)
        #self.board.attributes("-fullscreen", True)

        self.text = Tk()
        self.text_log = Text(self.text)
        self.text.protocol("WM_DELETE_WINDOW", self.on_text_exit)

        self.random_event_gen = RandomEvent()

        self.party_text = Tk()
        self.party_text_log = Text(self.party_text)
        self.party_text.protocol("WM_DELETE_WINDOW", self.on_party_exit)
        self.party = [Warrior("Warrior"), Monk("Monk"), Thief("Thief"), Mage("Mage")]

        self.current_row = 1
        self.current_col = 1
        self.current_floor = 1
        self.enemies_defeated = 0
        self.cheat_mode = False
        self.done = False

        self.matrix = [[Button(self.board, text="?") for i in range(3)] for i in range(3)]

        for i in range(3):
            for j in range(3):
                self.matrix[i][j].grid(row=i, column=j)

        self.matrix[0][0].bind('<Button-1>', lambda event: self.item_find(event, self.matrix[0][0]))
        self.matrix[0][1].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[0][1]))
        self.matrix[0][2].bind('<Button-1>', lambda event: self.item_find(event, self.matrix[0][2]))

        self.matrix[1][0].bind('<Button-1>', lambda event: self.found_stairs(event, self.matrix[1][0]))
        self.matrix[1][1].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[1][1]))
        self.matrix[1][2].bind('<Button-1>', lambda event: self.empty_room(event, self.matrix[1][2]))

        self.matrix[2][0].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[2][0]))
        self.matrix[2][1].bind('<Button-1>', lambda event: self.empty_room(event, self.matrix[2][1]))
        self.matrix[2][2].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[2][2]))

        self.initUI()

    def enter_room(self, button, room_text):
        self.current_row = button.grid_info()['row']
        self.current_col = button.grid_info()['column']
        button.config(text=room_text)
        self.text_log.pack()
        self.text_log.insert(INSERT, "Current Position: ")
        self.text_log.insert(INSERT, self.current_row)
        self.text_log.insert(INSERT, ' ')
        self.text_log.insert(INSERT, self.current_col)
        self.text_log.insert(END, "\n")
        self.party_stats()

    def enemy_encounter(self, event, button):
        self.enter_room(button, "battle")

        battle_window = Toplevel(self.board)
        app = Battle(self.party, self.cheat_mode, self.text_log, self.party_text_log, self.random_event_gen.get_enemy(),
                            battle_window, self)

    def item_find(self, event, button):
        self.enter_room(button, "item")
        temp = self.random_event_gen.get_item()
        self.text_log.pack()
        self.text_log.insert(INSERT, "Party Got: ")
        self.text_log.insert(INSERT, temp)
        self.text_log.insert(END, "\n")

        if temp == "HP+10":
            for i in range(len(self.party)):
                self.party[i].gain_hp(10)
        elif temp == "HP+30":
            for i in range(len(self.party)):
                self.party[i].gain_hp(30)
        elif temp == "Attack+1":
            for i in range(len(self.party)):
                self.party[i].gain_att(1)
        elif temp == "Attack+3":
            for i in range(len(self.party)):
                self.party[i].gain_att(3)
        elif temp == "Defense+1":
            for i in range(len(self.party)):
                self.party[i].gain_def(1)
        elif temp == "Defense+3":
            for i in range(len(self.party)):
                self.party[i].gain_def(3)
        elif temp == "Magic+1":
            for i in range(len(self.party)):
                self.party[i].gain_mag(1)
        elif temp == "Magic+3":
            for i in range(len(self.party)):
                self.party[i].gain_mag(3)
        else:
            pass

        self.party_stats()

    def empty_room(self, event, button):
        self.enter_room(button, "empty")

    def found_stairs(self, event, button):
        self.enter_room(button, "stairs")
        self.current_floor = self.current_floor + 1
        for i in range(3):
            for j in range(3):
                self.matrix[i][j].config(text="?")
        temp_i = randint(0, 2)
        temp_j = randint(0, 2)
        self.matrix[temp_i][temp_j].bind('<Button-1>', lambda event: self.found_stairs(event, self.matrix[temp_i][temp_j]))
        self.matrix[temp_i][temp_j].config(text="stairs")
        self.get_board_events()
        self.board.title("Dungeon Crawler Floor " + str(self.current_floor))

    def party_stats(self):
        self.party_text_log.delete('1.0', END)
        for i in range(len(self.party)):
            self.party_text_log.pack()
            self.party_text_log.insert(INSERT, self.party[i].name)
            self.party_text_log.insert(INSERT, ' ')
            self.party_text_log.insert(INSERT, self.party[i].hp)
            self.party_text_log.insert(END, "\n")

    def initUI(self):
        self.board.title("Dungeon Crawler Floor 1")
        menubar = Menu(self.board)
        self.board.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="New", command=self.onNew)
        fileMenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=fileMenu)
        enterMenu = Menu(menubar)
        enterMenu.add_command(label="Controls", command=self.onControl)
        enterMenu.add_command(label="Cheats", command=self.cheat)
        menubar.add_cascade(label="Help", menu=enterMenu)

    def onNew(self):
        self.current_row = 1
        self.current_col = 1
        self.current_floor = 1
        self.enemies_defeated = 0
        self.cheat_mode = False

        self.text_log.delete('1.0', END)
        self.party_text_log.delete('1.0', END)

        for i in range(3):
            for j in range(3):
                self.matrix[i][j].config(text="?")

        self.matrix[0][0].bind('<Button-1>', lambda event: self.item_find(event, self.matrix[0][0]))
        self.matrix[0][1].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[0][1]))
        self.matrix[0][2].bind('<Button-1>', lambda event: self.item_find(event, self.matrix[0][2]))

        self.matrix[1][0].bind('<Button-1>', lambda event: self.found_stairs(event, self.matrix[1][0]))
        self.matrix[1][1].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[1][1]))
        self.matrix[1][2].bind('<Button-1>', lambda event: self.empty_room(event, self.matrix[1][2]))

        self.matrix[2][0].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[2][0]))
        self.matrix[2][1].bind('<Button-1>', lambda event: self.empty_room(event, self.matrix[2][1]))
        self.matrix[2][2].bind('<Button-1>', lambda event: self.enemy_encounter(event, self.matrix[2][2]))

        for i in range(len(self.party)):
            self.party[i].reset_stats()

    def onControl(self):
        self.text_log.pack()
        self.text_log.insert(INSERT, "Click on the ? spaces to look for the stairs")

    def get_board_events(self):
        if self.matrix[0][0]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[0][0].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[0][0]))
            elif temp_num == 1:
                self.matrix[0][0].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[0][0]))
            elif temp_num == 2:
                self.matrix[0][0].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[0][0]))
            else:
                pass
        else:
            self.matrix[0][0].config(text="?")

        if self.matrix[0][1]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[0][1].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[0][1]))
            elif temp_num == 1:
                self.matrix[0][1].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[0][1]))
            elif temp_num == 2:
                self.matrix[0][1].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[0][1]))
            else:
                pass
        else:
            self.matrix[0][1].config(text="?")

        if self.matrix[0][2]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[0][2].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[0][2]))
            elif temp_num == 1:
                self.matrix[0][2].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[0][2]))
            elif temp_num == 2:
                self.matrix[0][2].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[0][2]))
            else:
                pass
        else:
            self.matrix[0][2].config(text="?")

        if self.matrix[1][0]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[1][0].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[1][0]))
            elif temp_num == 1:
                self.matrix[1][0].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[1][0]))
            elif temp_num == 2:
                self.matrix[1][0].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[1][0]))
            else:
                pass
        else:
            self.matrix[1][0].config(text="?")

        if self.matrix[1][1]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[1][1].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[1][1]))
            elif temp_num == 1:
                self.matrix[1][1].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[1][1]))
            elif temp_num == 2:
                self.matrix[1][1].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[1][1]))
            else:
                pass
        else:
            self.matrix[1][1].config(text="?")

        if self.matrix[1][2]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[1][2].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[1][2]))
            elif temp_num == 1:
                self.matrix[1][2].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[1][2]))
            elif temp_num == 2:
                self.matrix[1][2].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[1][2]))
            else:
                pass
        else:
            self.matrix[1][2].config(text="?")

        if self.matrix[2][0]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[2][0].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[2][0]))
            elif temp_num == 1:
                self.matrix[2][0].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[2][0]))
            elif temp_num == 2:
                self.matrix[2][0].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[2][0]))
            else:
                pass
        else:
            self.matrix[2][0].config(text="?")

        if self.matrix[2][1]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[2][1].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[2][1]))
            elif temp_num == 1:
                self.matrix[2][1].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[2][1]))
            elif temp_num == 2:
                self.matrix[2][1].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[2][1]))
            else:
                pass
        else:
            self.matrix[2][1].config(text="?")

        if self.matrix[2][2]['text'] != "stairs":
            temp_num = randint(0, 2)
            if temp_num == 0:
                self.matrix[2][2].bind('<Button-1>',
                                       lambda event: self.enemy_encounter(event, self.matrix[2][2]))
            elif temp_num == 1:
                self.matrix[2][2].bind('<Button-1>',
                                       lambda event: self.item_find(event, self.matrix[2][2]))
            elif temp_num == 2:
                self.matrix[2][2].bind('<Button-1>',
                                       lambda event: self.empty_room(event, self.matrix[2][2]))
            else:
                pass
        else:
            self.matrix[2][2].config(text="?")

    def on_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.done = True
            self.on_text_exit()
            self.on_party_exit()

            end_window = Toplevel(self.board)
            exit_text = "You made it to floor: " + str(self.current_floor)
            msg = Message(end_window, text=exit_text)
            msg.config(bg='orange', font=('helvetica', 24, 'bold'))
            msg.pack()

            self.board.after(3000, self.board.destroy)
        else:
            self.onNew()

    def on_text_exit(self):
        if self.done:
            self.text.destroy()

    def on_party_exit(self):
        if self.done:
            self.party_text.destroy()

    def cheat(self):
        self.cheat_mode = True

    def party_dead(self):
        if all(self.party[i].is_dead for i in range(len(self.party))):
            self.game_over()

    def game_over(self):
        loss_screen = Toplevel(self.board)

        width = loss_screen.winfo_screenwidth()
        height = loss_screen.winfo_screenheight()
        loss_screen.geometry('%dx%d+%d+%d' % (width * 0.8, height * 0.8, width * 0.1, height * 0.1))

        image_file = "game_over.png"

        image = PhotoImage(file=image_file)
        canvas = Canvas(loss_screen, height=height * 0.8, width=width * 0.8, bg="brown")
        canvas.create_image(width * 0.8 / 2, height * 0.8 / 2, image=image)
        canvas.pack()

        loss_screen.after(3000, loss_screen.destroy)
        self.on_exit()

    def run_board(self):
        self.board.mainloop()


def main():
    gb = GameBoard()
    gb.run_board()

main()
