from tkinter import *
from random import randint
from tkinter import filedialog as fd
from tkinter import messagebox as mb
root = Tk()
root.title('Space Adventure')

def open_recordfile():
    global best_s
    file_name = fd.askopenfilename()
    f = open(file_name)
    best_s = f.readline()
    f.close()
    c.create_text(1000, 20, fill="#00CCFF", text="Record: " + best_s, tag='record', font='Arial 30')

def save_recordfile():
    global best_s
    file_name = fd.asksaveasfilename()
    f = open(file_name, "w")
    f.write(best_s)
    f.close()

def spravka():
    mb.showinfo(title="Справка", message="Для передвижения звездолёта используйте стрелки на клавиатуре.\n"
                "Уклоняйтесь от метеоров, попытайтесь долететь как можно дальше.\n"
                "Нажав кнопку (Файл) вам откроется перечень дополнительных функций.\n"
                "Для сохранения вашего рекорда нажмите на (Сохранить).\n"
                "Для просмотра вашего сохранённого рекорда нажмите на (Загрузить).\n"
                "Приятной игры!")

mainmenu = Menu(root)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Сохранить", command=save_recordfile)
filemenu.add_command(label="Загрузить", command=open_recordfile)
filemenu.add_command(label="Справка", command=spravka)
filemenu.add_command(label="Настройки")
mainmenu.add_cascade(label="Файл", menu=filemenu)



vx = 0
vy = 0
def on_key_press(event):
    global vx, vy
    if event.keysym == "Up":
        vy = -10
    if event.keysym == "Down":
        vy = +10
    if event.keysym == "Right":
        vx = +10
    if event.keysym == "Left":
        vx = -10


def on_key_release(event):
    global vx, vy
    if event.keysym in ('Up', 'Down'):
        vy = 0
    if event.keysym in ('Left', 'Right'):
        vx = 0



def game_loop():
    c.move('plane', vx, vy)
    root.after(50, game_loop)

def stars_loop():
    c.move('stars', 0, 1)
    for star in stars:
        if c.coords(star)[1] > 900:
            x = randint(0, 1600)
            y = 0
            c.coords(star, x, y, x+2, y+2)
    root.after(50, stars_loop)

Time = True

def time():

    if Time:
        s['s'] += 1
        if s['s'] == 60:
            s['m'] += 1
            s['s'] = 0
        c.delete('timer')
        c.create_text(45, 20, fill="#00CCFF", text=f"{s['m']}:{'0' if s['s'] < 10 else ''}{s['s']}", tag='timer', font='Arial 30')

    root.after(1000, time)

def meteors_loop():
    c.move('meteors', 0, 2)
    global best_s
    for meteor in range(0, len(meteors), 4):
        x1, x2, x3, x4 = c.coords(pol)
        if c.coords(meteors[meteor])[1] > 900:
            x = randint(0, 1600)
            y = -100
            #c.coords(meteors[meteor], x, y, x+100, y+100)
            c.coords(meteors[meteor], x, y, x+50, y-50)
            c.coords(meteors[meteor+1], x+10+randint(0,5), y -50+10+randint(0,5), x + 50-35+10+randint(0,5), y-35+10+randint(0,5))
            c.coords(meteors[meteor+2], x+30+randint(0,5), y -50+40+randint(0,5), x + 50-25+randint(0,5), y-25+10+randint(0,5))
            c.coords(meteors[meteor+3], x+40+randint(0,5), y -50+15+randint(0,5), x + 50-25+10+randint(0,5), y-25+10+randint(0,5))

        if meteors[meteor] in c.find_overlapping(x1, x2, x3, x4):
            global Time
            Time = False
            c.delete('plane')
            t = Toplevel()
            l = Label(t, text="Game Over", font="Arial 150")
            t.resizable(False, False)
            t.geometry("+250+300")
            lr = Label(t, text=f"Your record: {s['m']}:{'0' if s['s'] < 10 else ''}{s['s']}", font="Arial 50")
            best_s = f"{s['m']}:{'0' if s['s'] < 10 else ''}{s['s']}"
            ex = Button(t, text="Exit", font="Arial 40", command=root.destroy)
            l.grid(row=0, column=0, columnspan=2)
            ex.grid(row=1, column=1)
            lr.grid(row=1, column=0)
            return



    root.after(10, meteors_loop)

def add_meteors():
    x = randint(0, 1600)
    y = randint(0, 900)
    meteors.append(c.create_oval(x, y - 1200, x + 50, y - 1150, fill="grey", tag="meteors"))
    meteors.append(c.create_oval(x + 10 + randint(0, 5), y - 1200 + 10 + randint(0, 5), x + 50 - 35 + 10 + randint(0, 5),y - 1150 - 35 + 10 + randint(0, 5), fill="#3C3C3C", tag="meteors"))
    meteors.append(c.create_oval(x + 30 + randint(0, 5), y - 1200 + 40 + randint(0, 5), x + 50 - 25 + randint(0, 5),y - 1150 - 25 + 10 + randint(0, 5), fill="#3C3C3C", tag="meteors"))
    meteors.append(c.create_oval(x + 40 + randint(0, 5), y - 1200 + 15 + randint(0, 5), x + 50 - 25 + 10 + randint(0, 5),y - 1150 - 25 + 10 + randint(0, 5), fill="#3C3C3C", tag="meteors"))
    root.after(10000, add_meteors)

s = {'m': 0, 's': 0}
best_s = ''
c = Canvas(root, width = 1600, height = 900, bg="#000000")


pol = c.create_rectangle(193, 450, 327, 350, fill="black", tag="plane")
stars = []
for i in range(550):
    x = randint(0, 1600)
    y = randint(0, 900)
    stars.append(c.create_oval(x, y, x+2, y+2, fill="#FFFFFF", tag="stars"))

#основа
c.create_oval(255, 350, 265, 450, fill="#0066FF", tag="plane")
#середина основы
c.create_oval(257, 360, 263, 415, fill="#00CCFF", tag="plane")
#хвост
c.create_oval(235, 436, 285, 445, fill="#0066FF", tag="plane")
#левое крыло
c.create_polygon(200, 400, 200, 390, 257, 377, 255, 405, fill="blue", width=30, tag="plane")
c.create_polygon(208, 397, 208, 392, 250, 383, 250, 400, fill="#00CCFF", width=20, tag="plane")
c.create_oval(193, 370, 200, 415, fill="#00008B", tag="plane")
#правое крыло
c.create_polygon(320, 400, 320, 390, 265, 377, 266, 405, fill="blue", width=30, tag="plane")
c.create_polygon(310, 397, 310, 392, 270, 383, 270, 400, fill="#00CCFF", width=20, tag="plane")
c.create_oval(320, 370, 327, 415, fill="#00008B", tag="plane")

meteors = []

for i in range(20):
    x = randint(0, 1600)
    y = randint(0, 900)
    meteors.append(c.create_oval(x, y-1200, x+50, y-1150, fill="grey", tag="meteors"))
    meteors.append(c.create_oval(x+10+randint(0,5), y - 1200+10+randint(0,5), x + 50-35+10+randint(0,5), y - 1150-35+10+randint(0,5), fill="#3C3C3C", tag="meteors"))
    meteors.append(c.create_oval(x+30+randint(0,5), y - 1200+40+randint(0,5), x + 50-25+randint(0,5), y - 1150-25+10+randint(0,5), fill="#3C3C3C", tag="meteors"))
    meteors.append(c.create_oval(x+40+randint(0,5), y - 1200+15+randint(0,5), x + 50-25+10+randint(0,5), y - 1150-25+10+randint(0,5), fill="#3C3C3C", tag="meteors"))
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

c.move('plane', 350, 0)
time()
game_loop()
stars_loop()
meteors_loop()
add_meteors()
c.pack()
root.mainloop()
