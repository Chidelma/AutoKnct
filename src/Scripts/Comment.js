export class Comment {

    constructor(data) {

        this.user_id = data.userID;
        this.text = data.text;
        this.date = data.date;
        this.name = data.name;
        this.autoID = data.autoID != null ? data.autoID : null;
    }
}