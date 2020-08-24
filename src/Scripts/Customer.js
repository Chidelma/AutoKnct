import { Message } from './Message';
import { Auto } from './Auto';

export class Customer {

    constructor(tokens, user, userID, garage) { 

        this.tokens = tokens != null ? tokens : null;
        this.isAuth = true;

        this.Name = user.Name;
        this.Email = user.Email;
        this.user_id = userID;
        this.Picture = user.Picture;
        this.Username = user.Username;
        this.Type = user.Type;

        this.compare = []; this.owned = []; this.shared = []; this.auction = []; this.messages = [];

        let i;

        if(garage != null) {
            console.log(garage);
            for(i = 0; i < garage.compare.length; i++) 
                this.compare.push(new Auto(garage.compare[i], garage.compare[i]._id));

            for(i = 0; i < garage.owned.length; i++)
                this.owned.push(new Auto(garage.owned[i], garage.owned[i]._id));

            for(i = 0; i < garage.shared.length; i++)
                this.shared.push(new Auto(garage.shared[i], garage.shared[i]._id));
            
            for(i = 0; i < garage.auction.length; i++)
                this.auction.push(new Auto(garage.auction[i], garage.auction[i]._id))

        } else {
            for(i = 0; i < user.compare.length; i++) 
                this.compare.push(new Auto(user.compare[i], user.compare[i]._id));

            for(i = 0; i < user.owned.length; i++)
                this.owned.push(new Auto(user.owned[i], user.owned[i]._id));

            for(i = 0; i < user.shared.length; i++)
                this.shared.push(new Auto(user.shared[i], user.shared[i]._id));

            for(i = 0; i < user.auction.length; i++)
                this.auction.push(new Auto(user.auction[i], user.auction[i]._id)) 
        }

        if(user.messages != null) {

            for(let i = 0; i < user.messages.length; i++) {

                let currMess = user.messages[i];
    
                this.messages.push(new Message(currMess.id, currMess.Name, currMess.Time, currMess.Message));
            }
        }
    }

    updateGarage(garage) {

        this.compare = []; this.owned = []; this.shared = []; this.messages = [];

        let i;

        for(i = 0; i < garage.compare.length; i++)
            this.compare.push(new Auto(garage.compare[i], garage.compare[i]._id));

        for(i = 0; i < garage.owned.length; i++)
            this.owned.push(new Auto(garage.owned[i], garage.owned[i]._id));

        for(i = 0; i < garage.shared.length; i++)
            this.shared.push(new Auto(garage.shared[i], garage.shared[i]._id));
    }
}