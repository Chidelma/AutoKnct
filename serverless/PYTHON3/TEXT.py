class Text:

    def __init__(self, id, name, date, text, autoID, VIN):

        self.userID = id.decode('utf-8')
        self.name = name.decode('utf-8')
        self.date = date.decode('utf-8')
        self.text = text.decode('utf-8')
        self.auto = autoID.decode('utf-8')
        self.VIN = VIN.decode('utf-8')