import datetime

# Package class to hold the package details
class Packages:
    def __init__(self, ID, street, city, state, zip_code, deadline, weight, notes, status="At the Hub"):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None
        self.deliveryTime = None

    def __str__(self):
        return (f"ID: {self.ID}, Address: {self.street}, {self.city}, {self.state}, {self.zip}, "
                f"Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, "
                f"Departure Time: {self.departureTime}, Delivery Time: {self.deliveryTime}")

    def statusUpdate(self, time_change):
        if self.deliveryTime is None:
            self.status = "At the hub"
        elif time_change < self.departureTime:
            self.status = "At the hub"
        elif time_change < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"
        if self.ID == 9 and time_change > datetime.timedelta(hours=10, minutes=20):
            self.street = "410 S State St"
            self.zip = "84111"