class WebResponse:
    def __init__(self, type, code, description):
        self.type = type
        self.code = code
        self.description = description

    def getTypeResponse(self, type):
        return f"Hello, my name is {self.name} and I am {self.age} years old."
    
    def getResponse(self, code):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

    def have_birthday(self):
        self.age += 1
        return f"Happy {self.age}th birthday, {self.name}!"