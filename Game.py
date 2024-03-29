import pygame
import random
import math
import Game

background_colour = (255, 255, 255)
(width, height) = (770, 520)
drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.005)
Game = None
touching = False




def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    Game.py: 14
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


def collideLine(particle, line): #checks if particle is touching a line
    touching = False
    px = particle.x
    py = particle.y

    xstart = line.xstart
    ystart = line.ystart
    xend = line.xend
    yend = line.yend

    pygame.draw.polygon(screen, (0, 0, 0), [[px, py], [xstart, ystart], [xend, yend]], 5)

    side1 = math.sqrt(((xstart-px)*(xstart-px))+((ystart-py)*(ystart-py)))
    side2 = math.sqrt(((xend-xstart)*(xend-xstart))+((yend-ystart)*(yend-ystart)))
    side3 = math.sqrt(((xend - px) * (xend - px)) + ((yend - py) * (yend - py)))

    semi = int((side1+side2+side3)/2)

    area = math.sqrt(abs((semi)*(semi-side1)*(semi-side2)*(semi-side3)))


    height = int((2*area)/side2)
    # print(xstart)
    # print(xend)
    # print(ystart)
    # print(yend)
    # print(py)
    # print(px)
    # print("cut")

    if px < xend and px > xstart or py < yend and py > ystart or py > yend and py < ystart or px > xend and px < xstart: #checks if particle is actually colliding with line and not a ghost line
        # print("ll")
        if height <= particle.size:
            touching = True
            # print(area)
            #
            # print ("works")
            # #print(height)

    #
        if touching == True: #computes the particle's new direction
            lineXCompenent = line.xend - line.xstart
            lineYCompenent = line.yend - line.ystart
            lineAngle = math.degrees(math.atan(lineYCompenent/lineXCompenent))

            particleAngle = math.degrees(particle.angle)

            angleDifferences = particleAngle - lineAngle
            newAngle = 180 + lineAngle - particleAngle
            particle.angle = math.radians(newAngle)
            return True
        return False


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, math.pi, 0.005)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


player = Particle(500, 500, 20)


class Line():
    def __init__(self, xstart, ystart, xend, yend):
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.thickness = 5
        self.color = (0, 0, 0)
        start = []
        end = []
    def draw(self):
        pygame.draw.line(screen, self.color, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.thickness)



        # for i in xstart:
        #     for j in ystart:
        #         start.append((xstart[i]), (ystart[j]))
        # for i in xend:
        #     for j in yend:
        #         end.append((xend[i]), (yend[j]))

                #establish points
        #take first two from each array and then draw a line between the two points
        #look at particle's drawing function
        #PURPOSE: create a line from those points

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 8')

# number_of_particles = 1
# my_particles = []

lines = []
#eventually import lines coords from Main here
lines.append(Line(400, 400, 300, 200))

lines.append(Line(50, 50, 200, 200))

touchedLine = []
for x in range(len(lines)):
    touchedLine.append(0)

# for n in range(number_of_particles):
#     size = random.randint(10, 20)
#     x = random.randint(size, width - size)
#     y = random.randint(size, height - size)
#
#     particle.speed = random.random()
#     particle.angle = random.uniform(0, math.pi * 2)
#
#     my_particles.append(particle)

player = Particle(500, 500, 20)

selected_particle = None
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = player
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    for i, Line in enumerate(lines):

        if touchedLine[i] < 0:
            #print(i)
            if collideLine(player, lines[i]) == True:
                touchedLine[i] = 10
                # print("l")

        touchedLine[i] -= 1
        lines[i].draw()

    player.move()
    player.bounce()
    player.display()

    pygame.display.flip()
