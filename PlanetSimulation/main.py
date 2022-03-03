import pygame
import math

pygame.init()

# Constants

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREY = (80, 80, 80)
LIGHT_ORANGE = (255, 204, 153)
BLACK = (0, 0, 0)


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")


class Star:

    # Constants

    AU = 149.6e6 * 1000    # Astronomical Units (km -> m)
    G = 6.67428e-11        # Universal gravitational constant
    SCALE = 200 / AU       # 1 AU = 100 px
    TIMESTEP =  3600 * 24  # 1 day in sec

    def __init__(self, x, y, radius, color, mass):

        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.mass = mass

        self.xVelocity = 0
        self.yVelocity = 0

        self.sun = False    # If the star is a sun
        self.distToSun = 0
        self.orbit = []

    def draw(self, window):
        x = self.x * self.SCALE + (WIDTH / 2)
        y = self.y * self.SCALE + (HEIGHT / 2)
        

        if len(self.orbit) >= 2:
            updated_orbit = []
            for point in self.orbit:
                xx, yy = point
                xx = xx * self.SCALE + WIDTH / 2
                yy = yy * self.SCALE + HEIGHT / 2
                updated_orbit.append((xx, yy))

            
            pygame.draw.lines(window, self.color, False, updated_orbit, 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if not self.sun:
            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            distText = pygame.font.Font.render(font, f"{round(self.distToSun/1000, 1)}km", True, WHITE)
            window.blit(distText, (x - distText.get_width() / 2, y - distText.get_height() / 2))


    def gravForce(self, other):
        otherX, otherY = other.x, other.y
        dist = math.sqrt(((otherX - self.x)**2) + ((otherY - self.y)**2))
        
        if other.sun:
            self.distToSun = dist

        force = self.G * self.mass * other.mass / dist**2
        theta = math.atan2(otherY - self.y, otherX - self.x)
        forceX = math.cos(theta) * force
        forceY = math.sin(theta) * force
        
        return forceX, forceY
    
    def updatePosition(self, stars):
        totalForceX = totalForceY = 0
        
        for star in stars:
            if self == star:
                continue
            fx, fy = self.gravForce(star)
            totalForceX += fx
            totalForceY += fy
        
        self.xVelocity += totalForceX / self.mass * self.TIMESTEP
        self.yVelocity += totalForceY / self.mass * self.TIMESTEP
        
        self.x += self.xVelocity * self.TIMESTEP
        self.y += self.yVelocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))
                
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Star(0, 0, 30, YELLOW, 1.98892 * (10**30))
    sun.sun = True

    mercury = Star(0.387 * Star.AU, 0, 12, DARK_GREY, 0.33 * (10**24))
    venus = Star(0.723 * Star.AU, 0, 14, LIGHT_ORANGE, 4.8685 * (10**24))
    earth = Star(Star.AU, 0, 16, BLUE, 5.9742 * (10**24))
    mars = Star(1.524 * Star.AU, 0, 12, RED, 6.39 * (10**23))
    
    # Initial velocity, otherwise the planets would be sucked by the sun
    
    mercury.yVelocity = 47.4 * 10**3
    venus.yVelocity = -35.02 * 10**3
    mars.yVelocity = 24.077 * 10**3
    earth.yVelocity = 29.783 * 10**3

    stars = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for star in stars:
            star.updatePosition(stars)
            star.draw(WINDOW)

        pygame.display.update()
    pygame.quit()


main()