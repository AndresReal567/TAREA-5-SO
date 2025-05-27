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
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return max(-self.max_steer, min(self.max_steer, output))

class LineFollowerCar:
    def __init__(self, canvas, track_items, start_line, laps_required, info_text):
        self.canvas = canvas
        self.track_items = track_items
        self.start_line = start_line
        self.laps_required = laps_required
        self.laps_completed = 0
        self.info_text = info_text

        self.car_x = 100
        self.car_y = 750  # Parte inferior del laberinto
        self.car_angle = -90  # Hacia arriba
        self.speed = 3
        self.sensor_dist = 30     # Adelantados
        self.sensor_offset = 25   # Más separados
        self.last_time = time.time()
        self.pid = PIDController(4.0, 0.001, 2.0, max_steer=8)

        self.body = canvas.create_polygon(0,0,0,0,0,0,0,0, fill='red', outline='black')
        self.wheels = [canvas.create_rectangle(0,0,0,0, fill='black') for _ in range(4)]
        self.sensors = [canvas.create_oval(0,0,0,0, fill='yellow') for _ in range(3)]

        self.update_car()

    def update_car(self):
        a = math.radians(self.car_angle)
        c, s = math.cos(a), math.sin(a)
        pts = [
            self.car_x + 20*c - 10*s, self.car_y + 20*s + 10*c,
            self.car_x + 20*c + 10*s, self.car_y + 20*s - 10*c,
            self.car_x - 20*c + 10*s, self.car_y - 20*s - 10*c,
            self.car_x - 20*c - 10*s, self.car_y - 20*s + 10*c
        ]
        self.canvas.coords(self.body, *pts)

        wheel_offsets = [(-18,-12),(-18,12),(18,-12),(18,12)]
        for wheel, (ox, oy) in zip(self.wheels, wheel_offsets):
            wx = self.car_x + ox*c - oy*s
            wy = self.car_y + ox*s + oy*c
            self.canvas.coords(wheel, wx-5, wy-5, wx+5, wy+5)

        for i, sensor in enumerate(self.sensors):
            offset = (i-1)*self.sensor_offset
            sx = self.car_x + self.sensor_dist*c - offset*s
            sy = self.car_y + self.sensor_dist*s + offset*c
            self.canvas.coords(sensor, sx-3, sy-3, sx+3, sy+3)

    def read_sensors(self):
        readings = []
        for i in range(3):
            a = math.radians(self.car_angle)
            c, s = math.cos(a), math.sin(a)
            offset = (i-1)*self.sensor_offset
            sx = self.car_x + self.sensor_dist*c - offset*s
            sy = self.car_y + self.sensor_dist*s + offset*c
            hits = self.canvas.find_overlapping(sx-2, sy-2, sx+2, sy+2)
            on_track = any(item in self.track_items for item in hits)
            self.canvas.itemconfig(self.sensors[i], fill='green' if on_track else 'yellow')
            readings.append(on_track)

        # Lógica mejorada
        if readings == [False, True, False]:
            return 0
        elif readings == [True, True, False]:
            return -0.5
        elif readings == [True, False, False]:
            return -1
        elif readings == [False, True, True]:
            return 0.5
        elif readings == [False, False, True]:
            return 1
        elif readings == [True, False, True]:
            return 0  # centro posiblemente
        else:
            return 0

    def check_start(self):
        x1, y1, x2, y2 = self.start_line
        margin = 15  # margen adicional por el grosor de la línea
        return (
            min(x1, x2) < self.car_x < max(x1, x2)
            and min(y1, y2) - margin < self.car_y < max(y1, y2) + margin
    )
s

    def move(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        err = self.read_sensors()
        steer = self.pid.compute(err, dt)
        self.car_angle += steer
        self.car_x += self.speed * math.cos(math.radians(self.car_angle))
        self.car_y += self.speed * math.sin(math.radians(self.car_angle))
        self.update_car()

        if self.check_start() and not getattr(self, '_crossed', False):
            self.laps_completed += 1
            self._crossed = True
            self.info_text.set(f"vuelta: {self.laps_completed}/{self.laps_required}")
        if not self.check_start():
            self._crossed = False

        if self.laps_completed < self.laps_required:
            window.after(20, self.move)
        else:
            self.info_text.set("🏁 termino!")

# GUI setup
window = tk.Tk()
window.title("🚗 Laberinto - Line Follower")
canvas = tk.Canvas(window, width=800, height=800, bg='white')
canvas.pack()

# LABERINTO
track_points = [
    100,750, 100,100, 700,100, 700,700, 200,700, 200,200,
    600,200, 600,600, 300,600, 300,300, 500,300, 500,500,
    400,500, 400,400
]
track_items = [canvas.create_line(*track_points, smooth=False, width=40, fill='black')]

# Línea de meta al final del laberinto (más ancha y atraviesa el camino completamente)
start_line = (350, 400, 450, 400)
canvas.create_line(start_line[0], start_line[1], start_line[2], start_line[3], fill='yellow', width=25)


# Label
laps_var = tk.StringVar()
laps_var.set("Lap: 0/1")
label = tk.Label(window, textvariable=laps_var, font=("Arial",18), bg='white', fg='black')
label.place(x=10,y=10)

# Iniciar carro
car = LineFollowerCar(canvas, track_items, start_line, laps_required=1, info_text=laps_var)
window.after(1000, car.move)
window.mainloop()
