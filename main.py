import tkinter as tk
import math
import time

class PIDController:
    def __init__(self, Kp, Ki, Kd, max_steer):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.max_steer = max_steer
        self.prev_error = 0
        self.integral = 0

    def compute(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt>0 else 0
        raw = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
        # Limita el ángulo de giro
        steer = max(-self.max_steer, min(self.max_steer, raw))
        self.prev_error = error
        return steer

class LineFollowerCar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.car_x = 200
        self.car_y = 140
        self.car_angle = 90
        self.speed = 3
        self.sensor_distance = 40
        self.pid = PIDController(Kp=1.2, Ki=0.0002, Kd=0.5, max_steer=5)
        self.last_time = time.time()
        # dibuja carro
        self.body        = canvas.create_polygon(0,0,50,0,50,30,0,30, fill='#f2f2f2', outline='#1B4F72')
        self.left_wheel  = canvas.create_oval(0,0,12,12, fill='#2C3E50')
        self.right_wheel = canvas.create_oval(0,0,12,12, fill='#2C3E50')
        self.sensor_dot  = canvas.create_oval(0,0,6,6, fill='red')
        self.update_car()

    def update_car(self):
        a = math.radians(self.car_angle); c, s = math.cos(a), math.sin(a)
        pts = [
            self.car_x+25*c -15*s, self.car_y+25*s +15*c,
            self.car_x+25*c +15*s, self.car_y+25*s -15*c,
            self.car_x-25*c +15*s, self.car_y-25*s -15*c,
            self.car_x-25*c -15*s, self.car_y-25*s +15*c
        ]
        self.canvas.coords(self.body, *pts)
        # ruedas
        wx, wy = self.car_x -12*s, self.car_y +12*c
        self.canvas.coords(self.left_wheel,  wx-6, wy-6, wx+6, wy+6)
        wx, wy = self.car_x +12*s, self.car_y -12*c
        self.canvas.coords(self.right_wheel, wx-6, wy-6, wx+6, wy+6)
        # sensor central
        fx = self.car_x + self.sensor_distance*c
        fy = self.car_y + self.sensor_distance*s
        self.canvas.coords(self.sensor_dot, fx-3, fy-3, fx+3, fy+3)

    def move(self):
        now = time.time(); dt = now - self.last_time; self.last_time = now
        # sensor central
        fx = self.car_x + self.sensor_distance*math.cos(math.radians(self.car_angle))
        fy = self.car_y + self.sensor_distance*math.sin(math.radians(self.car_angle))
        hits = self.canvas.find_overlapping(fx-6, fy-6, fx+6, fy+6)
        on_track = any(item in hits for item in track_items)
        error = (0.5 - (1 if on_track else 0)) * 10
        steer = self.pid.compute(error, dt)
        # aplicar giro y avance
        self.car_angle += steer
        self.car_x += self.speed * math.cos(math.radians(self.car_angle))
        self.car_y += self.speed * math.sin(math.radians(self.car_angle))
        # límites
        self.car_x = max(20, min(self.car_x, 780))
        self.car_y = max(20, min(self.car_y, 580))
        self.update_car()

window = tk.Tk()
window.title("Carro Seguidor — Tres Curvas Suaves")
canvas = tk.Canvas(window, width=800, height=600, bg='#1df5f5')
canvas.pack()

# Pista: tres loops con arcos
track_items = []
track_items.append(canvas.create_arc(100,200,300,400, start=0, extent=359, style=tk.ARC, outline='black', width=60))
track_items.append(canvas.create_arc(300,200,500,400, start=0, extent=359, style=tk.ARC, outline='black', width=60))
track_items.append(canvas.create_arc(500,200,700,400, start=0, extent=359, style=tk.ARC, outline='black', width=60))

# meta
canvas.create_oval(590,190,610,210, fill='green', outline='darkgreen')

car = LineFollowerCar(canvas)
def loop():
    car.move()
    window.after(20, loop)   # bucle más rápido
loop()
window.mainloop()

