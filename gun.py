from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)
G = 9.806

finished = False


def get_vel(vel):
    if abs(vel) < 0.3:
        return 0
    else:
        return vel


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.alive = True
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coordinates(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600)."""
        k = 0.7
        if self.x >= 800:
            self.vx = -abs(get_vel(k * self.vx))
        elif self.x <= 0:
            self.vx = abs(get_vel(k * self.vx))
        if self.y >= 600:
            self.vy = abs(get_vel(k * self.vy))
            self.vx = get_vel(k * self.vx)
        self.x += self.vx
        self.y -= self.vy
        self.vy = self.vy - G*0.03
        if self.vx**2 + self.vy**2 < 0.5:
            self.vx = self.vy = 0
            canvas.delete(self.id)
            self.alive = False

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        length = ((self.x - obj.x)**2 + (self.y - obj.y)**2) ** 0.5
        if length < obj.r + self.r:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canvas.create_line(20, 450, 50, 420, width=7)  # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, Bullet
        Bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        print(new_ball.vx, new_ball.vy)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.an),
                      450 + max(self.f2_power, 20) * math.sin(self.an)
                      )

    def power_up(self):
        if self.f2_on == 1:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.id_points = canvas.create_text(30, 30, text=self.points, font='28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        color = self.color = 'red'
        canvas.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)


t1 = Target()
screen1 = canvas.create_text(400, 300, text='', font='28')
g1 = Gun()
Bullet = 0
balls = []
targets = []


def txt_line(bullet):
    a = [11, 12, 13, 14]
    if 0 < bullet % 10 < 5 and a.count(bullet % 100) == 0:
        vys = 'выстрела'
    else:
        vys = 'выстрелов'
    return 'Вы уничтожили цель за ' + str(bullet) + ' ' + vys


def new_game():
    global g1, t1, screen1, balls, Bullet
    t1.new_target()
    Bullet = 0
    balls = []
    canvas.bind('<Motion>', g1.targetting)

    z = 0.03
    t1.live = 1
    while t1.live or balls:
        for b in balls:
            if not b.alive:
                balls.remove(b)
            b.move()
            b.set_coordinates()
            if b.hit_test(t1) and t1.live == 1:
                t1.live = 0
                t1.hit()
                canvas.itemconfig(screen1, text=txt_line(Bullet))
        canvas.update()
        canvas.bind('<Button-1>', g1.fire2_start)
        canvas.bind('<Motion>', g1.targetting)
        g1.power_up()
        canvas.bind('<ButtonRelease-1>', g1.fire2_end)
        time.sleep(z)
    canvas.itemconfig(screen1, text='')
    canvas.delete(Gun)
    root.after(5000, print('Hello!'))
    return


new_game()
root.mainloop()
