export class Auto {

    constructor(auto, autoID) {

        this._id = autoID;
        this.CYL = auto.CYL;
        this.Date = auto.Date;
        this.Mileage = auto.Mileage;
        this.Model = auto.Model;
        this.Price = auto.Price;
        this.Status = auto.Status;
        this.VIN = auto.VIN;
        this.Year = auto.Year;
        this.Images = auto.Images;
        this.Location = auto.Location != null ? auto.Location : null;
    }
        
}