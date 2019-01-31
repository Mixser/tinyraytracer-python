class Light(object):
    __slots__ = ('position', 'intensity')
    
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

