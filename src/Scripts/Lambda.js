import { currUser, storageKey } from './Init';

export function invokeLambda(api, load) {
    return new Promise((resolve, reject) => {

        load.env = window.location.hostname;

        currUser.update(state => {
            load.tokens = state.tokens || null;
            load.type = state.Type || null;
            return state;
        });

        if(typeof load.id == "undefined") {
            currUser.update(state => {
                load.id = state.user_id || sessionStorage.getItem(storageKey);
                return state;
            });
        }

        fetch(api, {
            method: 'post',
            body: JSON.stringify(load),
            headers: { 'Content-Type': 'application/json' },
            'Access-Control-Allow-Origin' : '*'
        })
        .then(res => 
            res.json()
        )
        .then(json => {
            resolve(json)
        })
        .catch(err => 
            reject(err)
        );
    });
}