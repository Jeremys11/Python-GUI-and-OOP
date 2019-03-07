from tkinter import *
from PIL import Image, ImageTk


class Battle:
    def __init__(self, party, cheat_mode, text_log, party_text_log, enemy, master, master_of_master):
        self.party = party
        self.enemy = enemy
        self.active = self.party[0]
        self.current_player = 0
        self.cheat_mode = cheat_mode
        self.master_of_master = master_of_master

        self.text_log = text_log
        self.party_text_log = party_text_log

        self.master = master
        self.frame = Frame(master)
        master.title("Battle")
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.frame.pack()

        self.image = Image.open(enemy.picture)
        self.photo = ImageTk.PhotoImage(self.image)

        # label with image
        self.l = Label(self.master, image=self.photo)
        self.l.pack()

        self.button1 = Button(self.frame, text='Attack', fg='red')
        self.button2 = Button(self.frame, text='Defend', fg='blue')
        self.button3 = Button(self.frame, text='Magic', fg='green')

        self.button1.grid(column=0, row=0)
        self.button2.grid(column=0, row=1)
        self.button3.grid(column=0, row=2)

        self.button1.bind('<Button-1>', lambda event: self.on_attack(event))
        self.button2.bind('<Button-1>', lambda event: self.on_defend(event))
        self.button3.bind('<Button-1>', lambda event: self.on_magic(event))


    def close_window(self):
        self.master.destroy()

    def on_attack(self, event):
        self.enemy.take_damage(self.active.attack)
        self.enemy.die()
        self.party_stats()
        if self.enemy.is_dead:
            self.splash_win()
        else:
            self.enemy_attack()

    def on_defend(self, event):
        self.defending = True
        self.party_stats()
        self.enemy_attack()

    def on_magic(self, event):
        self.enemy.take_magic_damage(self.active.magic)
        self.enemy.die()
        self.party_stats()
        if self.enemy.is_dead:
            self.splash_win()
        else:
            self.enemy_attack()

    def enemy_attack(self):
        self.party[self.current_player].take_damage(self.enemy.attack)
        self.party[self.current_player].die()
        self.party_stats()
        self.get_next_player()

    def splash_win(self):
        win_screen = Toplevel(self.master)

        width = win_screen.winfo_screenwidth()
        height = win_screen.winfo_screenheight()
        win_screen.geometry('%dx%d+%d+%d' % (width * 0.8, height * 0.8, width * 0.1, height * 0.1))

        image_file = "you_win.png"

        image = PhotoImage(file=image_file)
        canvas = Canvas(win_screen, height=height * 0.8, width=width * 0.8, bg="brown")
        canvas.create_image(width * 0.8 / 2, height * 0.8 / 2, image=image)
        canvas.pack()

        win_screen.after(3000, win_screen.destroy)
        self.close_window()

    def party_stats(self):
        self.party_text_log.delete('1.0', END)
        for i in range(len(self.party)):
            self.party_text_log.pack()
            self.party_text_log.insert(INSERT, self.party[i].name)
            self.party_text_log.insert(INSERT, ' ')
            self.party_text_log.insert(INSERT, self.party[i].hp)
            self.party_text_log.insert(END, "\n")
        self.party_text_log.pack()
        self.party_text_log.insert(INSERT, self.enemy.name)
        self.party_text_log.insert(INSERT, ' ')
        self.party_text_log.insert(INSERT, self.enemy.hp)
        self.party_text_log.insert(END, "\n")

    def get_next_player(self):
        if all(self.party[i].is_dead for i in range(len(self.party))):
            self.game_over()
        else:
            self.current_player = (self.current_player + 1) % 4
            while self.party[self.current_player].is_dead:
                self.current_player = (self.current_player + 1) % 4

    def game_over(self):
        self.master_of_master.game_over()
        self.close_window()

    def on_exit(self):
        if self.cheat_mode:
            self.close_window()