export class ChartPlot {

    constructor(leftX, bottomY, rightX) {

        this.leftX = [];
        this.bottomY = [];
        this.rightX = [];

        let i;

        for(i = 0; i < leftX.length; i++)
            this.leftX.push(leftX[i]);

        for(i = 0; i < bottomY.length; i++)
            this.bottomY.push(bottomY[i]);

        if(rightX != null) {
            for(i = 0; i < rightX.length; i++)
                this.rightX.push(rightX[i]);
        }
    }
}