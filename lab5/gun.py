from random import randrange as rnd, choice, randint
import tkinter as tk
import math
import time


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)
G = 9.806


def get_vel(vel):
    if abs(vel) < 0.3:
        return 0
    else:
        return vel


def mod_abs(one, two):
    if abs(one) > abs(two):
        return one
    else:
        return two


def define_angle(dy, dx):
    if dx == 0:
        dx += 10**(-5)
    angle = math.atan(dy / dx)
    if dx < 0:
        angle -= math.pi
    return angle


class Ball:
    def __init__(self, x, y):
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
        self.vy = self.vy - G*2*delta_t
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


class Bomb:
    def __init__(self, x, y):
        """ Конструктор класса bomb
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 7
        self.vx = 0
        self.vy = 0
        self.alive = True
        self.color = choice(['yellow', 'brown', 'black'])
        self.id = canvas.create_rectangle(
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
        self.vy = self.vy - G * 0.1
        if self.vx ** 2 + self.vy ** 2 < 0.5:
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
        length = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
        if length < obj.r + self.r:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.x = 20
        self.y = 450
        self.id = canvas.create_line(self.x, self.y, self.x + 20, self.y + 20, width=5)
        self.kx, self.ky = 1, 1

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, Bullet
        Bullet += 1
        new_ball = Ball(self.x + mod_abs(self.f2_power, 20) * math.cos(self.an),
                        self.y + mod_abs(self.f2_power, 20) * math.sin(self.an))
        new_ball.r += 5
        self.an = define_angle(event.y - self.y, event.x - self.x)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def fire_another(self, event):
        """
        Выстрел шаром другого типа
        :param event:
        :return:
        """
        global bombs, Bullet
        Bullet += 1
        new_bomb = Bomb(self.x + mod_abs(self.f2_power, 20) * math.cos(self.an),
                        self.y + mod_abs(self.f2_power, 20) * math.sin(self.an))
        new_bomb.r += 5
        self.an = define_angle(event.y - self.y, event.x - self.x)
        new_bomb.vx = self.f2_power * math.cos(self.an)
        new_bomb.vy = - self.f2_power * math.sin(self.an)
        bombs += [new_bomb]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = define_angle(event.y - self.y, event.x - self.x)
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, self.x, self.y,
                      self.x + max(self.f2_power, 20) * math.cos(self.an),
                      self.y + max(self.f2_power, 20) * math.sin(self.an)
                      )

    def power_up(self):
        if self.f2_on == 1:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')

    def move(self):
        self.x += self.kx * 3
        self.y += self.ky * 3
        canvas.coords(self.id, self.x, self.y,
                      self.x + max(self.f2_power, 20) * math.cos(self.an),
                      self.y + max(self.f2_power, 20) * math.sin(self.an)
                      )

    def move_left(self, event):
        self.kx, self.ky = -1, 0
        self.move()

    def move_right(self, event):
        self.kx, self.ky = 1, 0
        self.move()

    def move_up(self, event):
        self.kx, self.ky = 0, -1
        self.move()

    def move_down(self, event):
        self.kx, self.ky = 0, 1
        self.move()


class Target1:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(5, 50)
        self.vx = rnd(1, 7)
        self.vy = rnd(1, 7)
        color = self.color = 'red'
        canvas.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points

    def move(self):
        if self.x >= 800:
            self.vx = -abs(get_vel(self.vx))
        elif self.x <= 0:
            self.vx = abs(get_vel(self.vx))
        if self.y >= 600:
            self.vy = abs(get_vel(self.vy))
            self.vx = get_vel(self.vx)
        elif self.y <= 0:
            self.vy = -abs(get_vel(self.vy))
        self.x += self.vx
        self.y -= self.vy

    def set_coordinates(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )


class Target2:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canvas.create_rectangle(0, 0, 0, 0)
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(5, 50)
        self.vx = rnd(1, 7)
        self.vy = rnd(1, 7)
        color = self.color = 'blue'
        canvas.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points

    def move(self):
        accel = rnd(-10, 10)
        self.vx += accel*delta_t
        self.vy += accel*delta_t
        if self.x >= 800:
            self.vx = -abs(get_vel(self.vx))
        elif self.x <= 0:
            self.vx = abs(get_vel(self.vx))
        if self.y >= 600:
            self.vy = abs(get_vel(self.vy))
            self.vx = get_vel(self.vx)
        elif self.y <= 0:
            self.vy = -abs(get_vel(self.vy))
        self.x += self.vx
        self.y -= self.vy

    def set_coordinates(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )


screen1 = canvas.create_text(400, 300, text='', font='28')
g1 = Gun()
Bullet = 0
balls = []
bombs = []
targets = []
delta_t = 0.035


def txt_line(bullet):
    a = [11, 12, 13, 14]
    if bullet % 10 == 1 and a.count(bullet % 100) == 0:
        vys = 'выстрел'
    elif 1 < bullet % 10 < 5 and a.count(bullet % 100) == 0:
        vys = 'выстрела'
    else:
        vys = 'выстрелов'
    return 'Вы уничтожили цели за ' + str(bullet) + ' ' + vys


def alive_or_not(tars):
    alive = 0
    for t in tars:
        alive += int(t.live)
    if alive > 0:
        return True
    else:
        return False


def new_game():
    global g1, targets, screen1, balls, Bullet, bombs
    targets = []
    for i in range(randint(3, 7)):
        if randint(1, 2) == 1:
            t = Target1()
        else:
            t = Target2()
        t.live = 1
        targets.append(t)
    Bullet = 0
    balls = []
    bombs = []
    canvas.bind('<Motion>', g1.targetting)
    k = 0

    while alive_or_not(targets) or balls or bombs:
        for t in targets:
            t.move()
            if t.live == 1:
                t.set_coordinates()
            for bullets in [balls, bombs]:
                for b in bullets:
                    if not b.alive:
                        bullets.remove(b)
                    b.move()
                    b.set_coordinates()
                    if b.hit_test(t) and t.live == 1:
                        t.live = 0
                        t.hit()
            if not alive_or_not(targets):
                if k == 0:
                    canvas.itemconfig(screen1, text=txt_line(Bullet))
                k += 1
        canvas.update()
        canvas.bind('<Button-1>', g1.fire2_start)
        canvas.bind('<Button-3>', g1.fire2_start)
        canvas.bind('<Motion>', g1.targetting)
        g1.power_up()
        canvas.bind('<ButtonRelease-1>', g1.fire2_end)
        canvas.bind('<ButtonRelease-3>', g1.fire_another)
        root.bind('w', g1.move_up)
        root.bind('a', g1.move_left)
        root.bind('s', g1.move_down)
        root.bind('d', g1.move_right)
        time.sleep(delta_t)
    canvas.itemconfig(screen1, text='')
    canvas.delete(Gun)
    root.after(5000, new_game())
    return


new_game()
root.mainloop()
