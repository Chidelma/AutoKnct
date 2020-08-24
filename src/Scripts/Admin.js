import { Customer } from './Customer';

export class Admin extends Customer {

    constructor(tokens, keyCode, user, userID, garage) {
        super(tokens, user, userID, garage);

        this.keyCode = keyCode != null ? keyCode : null;
        this.DOB = user.D.O.B;
    }
}