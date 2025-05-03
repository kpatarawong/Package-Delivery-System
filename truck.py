# Truck class to hold truck details and track its progress
class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return f"Speed: {self.speed}, Miles: {self.miles}, Location: {self.currentLocation}, Time: {self.time}"
