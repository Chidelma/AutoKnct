import { Customer } from './Customer';

export class Business extends Customer {

    constructor(token, user, userID, garage) {
        super(token, user, userID, garage);

        this.business_name = user.BusinessName;
        this.customer_id = user.CustomerID;
        this.auction_cars = user.Auctions;
    }
}