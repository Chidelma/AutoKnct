from imports import uuid

class Customer:

    def __init__(self, name, email, username, picture):
        self.UserId = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(username)))
        self.Name = name.decode('utf-8')
        self.Email = email.decode('utf-8')
        self.Picture = picture.decode('utf-8') if picture != None else None
        self.Username = username.decode('utf-8')
        self.Type = 'CUSER'.decode('utf-8')


class Business(Customer):

    def __init__(self, name, email, username, Id, businessName, picture):
        super().__init__(name, email, username, picture)

        self.UserId = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(Id)))
        self.BusinessName = businessName.decode('utf-8')
        self.CustomerId = Id.decode('utf-8')
        self.Type = 'BUSER'.decode('utf-8')


class Admin(Customer):

    def __init__(self, name, email, username, dob, picture, role):
        super().__init__(name, email, username, picture)

        self.Dob = dob
        self.Role = role
        self.Type = 'AUSER'.decode('utf-8')