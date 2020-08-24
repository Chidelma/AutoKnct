import { Auto } from './Auto';

export class Search {

    constructor() {

        this.saved = false;
        this.results = [];
        this.prevResults = [];
        this.count = 0;
        this.userInput = '';
        this.sort = 'Model';
        this.order = 'asc';
        this.xValues = []; this.xValuesPrev = [];
        this.leftYValues = []; this.leftYValuesPrev = [];
        this.rightYValues = []; this.rightYValuesPrev = [];

        this.filters = {};
    }

    resultInit(data) {

        let i;

        for (i = 0; i < data.length; i++) {
            this.results.push(new Auto(data[i], data[i]._id));
            this.prevResults.push(new Auto(data[i], data[i]._id));
        }
    }
}
