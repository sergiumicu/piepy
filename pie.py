from math import cos, sin, pi
from random import random

#generates a random number in steps
def _random_with_steps() -> int:
    return (int(random() * 127) + 129)//10 * 10

#generates a random color
def random_color() -> str:
    return("rgb({}, {}, {})".format(_random_with_steps(), _random_with_steps(), _random_with_steps()))

#contains elements of the chart
class Element:
    def __init__(self, value: float = 0, name: str = None, color: str = None) -> None:
        self.value = value
        self.name = name
        self.color = color if color else random_color()

class Chart:
    def __init__(self) -> None:
        self.elements = []
    
    #function called to add an element to the chart
    def add_element(self, value: float, name: str = None, color: str = None) -> Element:
        to_add = Element(value, name, color)
        self.elements.append(to_add)

        return to_add

    #function called to remove an element from the chart
    def remove_element(self, index: int or list[int]) -> Element or list[Element] :
        if type(index) == int:
            return self.elements.pop(index)
        else:
            to_ret = []
            for i in index:
                self.elements.pop(i)
            return to_ret

    #sorts the chart elements: this makes the resulting pie chart large elements clump together
    def sort(self) -> None:
        self.elements.sort(key=lambda el: el.value)

    #get the total value of the elements in the chart
    def total(self) -> float:
        total = 0
        for el in self.elements:
            total += el.value
        return total

    #get the names used by the slices
    def get_names(self) -> list:
        nams = []
        for el in self.elements:
            nams.append(el.name)
        return nams

    #get the values used by the slices
    def get_values(self) -> list:
        vals = []
        for el in self.elements:
            vals.append(el.value)
        return vals

    #get the colors used by the slices
    def get_colors(self) -> list:
        cols = []
        for el in self.elements:
            cols.append(el.color)
        return cols

    #draws to a file with a few options
    def draw_to_file(self, fil: str = "pie.svg", size: int = 200, stroke: str = "", stroke_width: float = "") -> None:
        with open(fil, 'w') as pie:
            pie.write('''<?xml version="1.0" standalone="no"?><svg width="{}px" height="{}px" version="1.1" xmlns="http://www.w3.org/2000/svg">'''.format(size, size))

            pie.write('''<g transform="rotate({}, {}, {})">'''.format(360 * random(), size/2, size/2))

            total = self.total()

            #draw slices
            last_x = 5 * size/6
            last_y = size/2
            last_theta = 0

            for el in self.elements:
                theta = 2 * pi * el.value/total + last_theta

                new_x = size * 1/3 * cos(theta) + size/2
                new_y = size * 1/3 * sin(theta) + size/2

                pie.write('''<path d="M {} {} L {} {} A {} {} 0 {} 1 {} {} L {} {}" fill="{}" stroke="{}" stroke-width="{}" stroke-linecap="round"/>'''.format(size/2, size/2, 
                                                                                                 last_x, last_y, 
                                                                                                 size * 1/3, size * 1/3, 1 if theta - last_theta > pi else 0, new_x, new_y,
                                                                                                 size/2, size/2,
                                                                                                 el.color, stroke, str(stroke_width) + ("px" if len(str(stroke_width)) > 0 else "")))

                last_theta = theta
                last_x = new_x
                last_y = new_y

            pie.write('</g></svg>')
