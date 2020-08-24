export class User {

    constructor() {
        this.isAuth = false;
    }

    setTokens(data) {
        this.tokens = data.tokns != null ? data.tokns : data;
    }

    setKeyCode(data) {
        this.keyCode = data.key != null ? data.key : null;
    }
}