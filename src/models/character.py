character_list = []
class Character:
    name: str
    height: str
    mass: str
    haircolor: str
    skincolor: str
    eyecolor: str
    birthyear: str
    gender: str
    homeworld: str
    isActive: bool

    def __init__(self, name: str, height: str, mass: str, haircolor: str, skincolor: str, eyecolor: str, birthyear: str, gender: str, homeworld: str):
        self.name = name
        self.height = height
        self.mass = mass
        self.haircolor = haircolor
        self.skincolor = skincolor
        self.eyecolor = eyecolor
        self.birthyear = birthyear
        self.gender = gender
        self.homeworld = homeworld
        self.isActive = True
