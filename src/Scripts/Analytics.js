import { Auto } from './Auto';
import { Comment } from './Comment';

export class Analytix {

    constructor(data) {

        this.autoHist = [];

        let i;

        for(i = 0; i < data.listGarage.length; i++) 
            this.autoHist.push(new Auto(data.listGarage[i], data.listGarage[i]._id));

        this.numAucts = data.count;
        this.minBid = data.minBid;
        this.maxBid = data.maxBid;
        this.avgBidPrice = data.avgBidPrice;
        this.avgSalePrice = data.avgSalePrice;
        this.extData = data.extData;
        this.chartList = data.listChart;

        this.comments = [];

        if(data.comments != null) {
            for(i = 0; i < data.comments.length; i++)
                this.comments.push(new Comment(data.comments[i]));
        }
    }

    setComments(comments) {

        for(let i = 0; i < comments.length; i++) 
            this.comments.push(new Comment(comments[i]));
    }
}