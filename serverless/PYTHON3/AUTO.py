class Auto:

    def __init__(self, auto):

        self._id = auto['_id'].decode('utf-8')
        self.Model = auto['Model'].decode('utf-8')
        self.Year = auto['Year']
        self.Status = auto['Status'].decode('utf-8')
        self.Images = auto['Images']
        self.CYL = auto['CYL'].decode('utf-8')
        self.Date = auto['Date'].decode('utf-8')
        self.Mileage = auto['Mileage']
        self.Price = auto['Price']
        self.VIN = auto['VIN'].decode('utf-8')