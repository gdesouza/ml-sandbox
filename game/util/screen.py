from util.colour import Colour

class Screen:
    def __init__(self, width=800, height=600, colour=Colour.WHITE) -> None:
        self.width = width
        self.height = height
        self.background = colour

    def CenterWidth(self) -> int:
        return self.width/2
    
    def CenterHeight(self) -> int:
        return self.height/2