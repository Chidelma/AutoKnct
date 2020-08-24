import { Auto } from './Auto';

export class Home {

    constructor() { 

        this.saved = false;
        this.next = [];
    }

    initHome(data) {

        this.saved = true;

        for(let i = 0; i < data.length; i++) {
            this.next.push(new Auto(data[i], data[i]._id))
        }
    }
}