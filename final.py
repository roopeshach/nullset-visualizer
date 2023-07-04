import math
import random
from colorsys import hsv_to_rgb


class Circle:
    """
    A circle with a radius and a list of other circles placed inside it.
    Args:
        radius (float): The radius of the circle.
    
    """
    def __init__(self, radius):
        self.radius = radius
        self.contents = []  # [Placement]

    def add(self, circle, pos):
        """
        Adds a circle to the list of circles inside this circle.
        Args:
            circle (Circle): The circle to add.
            pos (tuple): The position of the circle relative to this circle.
        """

        self.contents.append(Placement(circle, pos))

class Placement:
    """
    A circle placed inside another circle.
    Args:
        circle (Circle): The circle being placed.
        pos (tuple): The position of the circle relative to the circle it is being placed in.
    """

    def __init__(self, circle, pos):
        self.circle = circle
        self.pos = pos

# make 0 and 1
cache = {0: Circle(.5), 1: Circle(1.)}
cache[1].add(cache[0], (-.5, 0))

def make(n):
    """
    Makes a circle with n circles inside it.
    Args:
        n (int): The number of circles to place inside the circle.
    Returns:
        Circle: The circle with n circles inside it.
    """

    if n in cache:
        return cache[n]

    a = make(n - 1)
    b = make(n - 2)
    z = Circle(a.radius + b.radius)
    z.add(a, (-b.radius, 0))
    z.add(b, (a.radius, 0))

    if n - 3 >= 0:
        c = make(n - 3)
        p = getnestpos(a, b, c)
        z.add(c, p)

        nest(z, n - 4, b, a)
    
    cache[n] = z
    return z

def nest(z, n, a, b, recurse=True):
    """
    Places a circle inside another circle.
    Args:
        z (Circle): The circle to place the circle inside.
        n (int): The number of circles to place inside the circle.
        a (Circle): The circle to place inside the other circle.
        b (Circle): The circle to place the other circle inside.
        recurse (bool): Whether to call nest recursively.
    """

    if n >= 0:
        ap = bp = None
        for q in z.contents:
            if q.circle is a:
                ap = q
            if q.circle is b:
                bp = q
        assert ap and bp, 'failed to find ap and bp'

        c = make(n)
        p = getnestpos(a, b, c, ap, bp)
        z.add(c, p)

        if recurse:
            nest(z, n - 1, a, c, recurse=False)
            nest(z, n - 2, c, b)

def getnestpos(a, b, c, ap=None, bp=None):
    """
    Gets the position of c relative to a.
    Args:
        a (Circle): The circle that c is being placed inside.
        b (Circle): The circle that c is being placed outside of.
        c (Circle): The circle that is being placed inside a.
        ap (Placement): The placement of a relative to b.
        bp (Placement): The placement of b relative to a.
    Returns:
        tuple: The position of c relative to a.
    """

    # use law of cosines to get angle between a->b and a->c
    p = a.radius ** 2 + a.radius * b.radius + a.radius * c.radius
    angle = math.acos((p - b.radius * c.radius) / (p + b.radius * c.radius))
    # find the vector a->c
    x = (a.radius + c.radius) * math.cos(angle) - b.radius
    y = (a.radius + c.radius) * math.sin(angle)
    
    if ap and bp:
        # place the vector correctly
        vx = bp.pos[0] - ap.pos[0]
        vy = bp.pos[1] - ap.pos[1]
        angle = math.atan2(vy, vx)
        vmag = math.hypot(vx, vy)
        vx -= a.radius * vx / vmag
        vy -= a.radius * vy / vmag
        
        x, y = (
            ap.pos[0] + vx + x * math.cos(angle) - y * math.sin(angle),
            ap.pos[1] + vy + x * math.sin(angle) + y * math.cos(angle)
        )
        
    return (x, y)


def printsvg(c, pos, file):
    """
    Prints a circle to an svg file.
    Args:
        c (Circle): The circle to print.
        pos (tuple): The position of the circle relative to the svg file.
        file (file): The file to print to.
    """

    # Generate a random color for the circle
    hue = random.uniform(10, 20)
    saturation = random.uniform(0, 1)
    value = random.uniform(0.6, 1)
    r, g, b = [int(255 * i) for i in hsv_to_rgb(hue, saturation, value)]
    color = f"rgb({r},{g},{b})"
    
    file.write('<circle cx="%f" cy="%f" r="%f" fill="%s" stroke="black" />\n' % (zoom * pos[0], zoom * pos[1], zoom * c.radius, color))
    
    for p in c.contents:
        printsvg(p.circle, (pos[0] + p.pos[0], pos[1] + p.pos[1]), file)


zoom = 5
c = make(10)

size = zoom * c.radius * 2
with open('output.svg', 'w') as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" width="%f" height="%f">\n' % (size, size))
    printsvg(c, (c.radius, c.radius), f)
    f.write('</svg>')