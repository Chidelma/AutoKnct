import { Customer } from './Customer';
import { Admin } from './Admin';
import { Business } from './Business';
import { currUser } from './Init';
import { User } from './User';

export function userInit(userID, user, garage) {

    if(user.Type[0] == 'A') {
        currUser.update(state => {
            state = new Admin(state.tokens || user.tokens, state.keyCode, user, userID, garage);
            return state;
        });
    } else if (user.Type[0] == 'B') {
        currUser.update(state => {
            state = new Business(state.tokens || user.tokens, user, userID, garage);
            return state;
        });
    } else if (user.Type[0] == 'C') {
        currUser.update(state => {
            state = new Customer(state.tokens || user.tokens, user, userID, garage);
            return state;
        });
    }
}

export function userExit() {

    currUser.update(state => {
        state = new User();
        return state;
    })
}