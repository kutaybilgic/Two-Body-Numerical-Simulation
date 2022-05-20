from dataclasses import dataclass
import math


@dataclass
class TwoBodyModel:
    coordinates: tuple  # (x,y)
    velocity: tuple


class TwoBodyController:
    eccentricity = 0.0
    mass_ratio = 0.0
    u = []
    du = [0, 0, 0, 0]

    def __init__(self, eccen, mass):
        self.mass_ratio = mass
        self.eccentricity = eccen
        self.u = [1, 0, 0, math.sqrt((1 + self.mass_ratio) * (1 + self.eccentricity))]

    body1 = TwoBodyModel((1, 0), (0, math.sqrt(
        (1 + mass_ratio) * (1 + eccentricity))))
    body2 = TwoBodyModel((1, 0), (0, math.sqrt(
        (1 + mass_ratio) * (1 + eccentricity))))

    def radius(self, x, y):
        return math.sqrt(pow(x, 2) + pow(y, 2))

    def dif(self):
        r = self.radius(self.u[0], self.u[1])
        for i in range(2):
            self.du[i] = self.u[i + 2]
            self.du[i + 2] = -(1+self.mass_ratio)*(self.u[i])/pow(r, 3)

    def euler(self, h):
        for i in range(4):
            self.dif()
            self.u[i] += h * self.du[i]

    def convert(self):
        self.body1.coordinates = (-1.0*(self.mass_ratio/(1 + self.mass_ratio))
                                  * self.u[0], -1.0*(self.mass_ratio/(1+self.mass_ratio)) * self.u[1])
        self.body2.coordinates = (
            (1/(1+self.mass_ratio)) * self.u[0], (1/(1+self.mass_ratio)) * self.u[1])

    def runge(self, h):
        a = [h/2, h/2, h, 0]
        b = [h/6, h/3, h/3, h/6]
        u0 = []
        ut = []
        dimension = len(self.u)

        for i in range(dimension):
            u0.append(self.u[i])
            ut.append(0)

        for j in range(4):
            du = self.derivative()
            for i in range(dimension):
                self.u[i] = u0[i] + a[j] * du[i]
                ut[i] = ut[i] + b[j] * du[i]

        for i in range(dimension):
            self.u[i] = u0[i] + ut[i]

    def derivative(self):
        du = [0, 0, 0, 0]
        rr = math.sqrt( math.pow(self.u[0],2) + math.pow(self.u[1],2))
        for i in range(2):
            du[i] = self.u[i + 2]
            du[i + 2] = -(1+self.mass_ratio)* self.u[i] / pow(rr, 3)

        return du


class App:
    choice = int(input("enter 1 for euler, enter 2 for runge: "))
    time_step = float(input("enter time step: "))
    tlast = float(input("enter tlast: "))
    size = 1+math.floor(tlast/time_step)
    mas_ratio = float(input("enter mass ratio : "))
    ecce = float(input("enter eccentricity: "))
    body_contr = TwoBodyController(ecce, mas_ratio)

    def run_euler(self):
        first = []
        second = []

        self.body_contr.convert()

        for i in range(self.size):
            first.append(self.body_contr.body1.coordinates)
            second.append(self.body_contr.body2.coordinates)
            self.body_contr.euler(self.time_step)
            self.body_contr.convert()

        wr = open("coordinates.txt", "w")

        for i in range(len(first)):
            wr.write(str(first[i][0]) + "," + str(first[i][1]) + "," + str(second[i][0]) + "," + str(second[i][1]) + "\n")
        wr.close()

    def run_runge(self):
        first = []
        second = []

        self.body_contr.convert()
        for i in range(self.size):
            first.append(self.body_contr.body1.coordinates)
            second.append(self.body_contr.body2.coordinates)
            self.body_contr.runge(self.time_step)
            self.body_contr.convert()

        wr = open("coordinates.txt", "w")

        for i in range(len(first)):
            wr.write(str(first[i][0]) + "," + str(first[i][1]) + "," + str(second[i][0]) + "," + str(second[i][1]) + "\n")
        wr.close()

    def run(self):
        if self.choice == 1:
            self.run_euler()
        elif self.choice == 2:
            self.run_runge()
        else:
            print("wrong !!!")


app = App()
app.run()
