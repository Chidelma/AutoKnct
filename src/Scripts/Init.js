import { writable } from 'svelte/store';
import { User } from './User';
import uuidv5 from 'uuid/v5';
import { Home } from './Home';
import { userExit, userInit } from './Entry';
import { Search } from './Search';

export let currUser = writable(new User());

export let homeTab = writable(new Home());

export let searchTab = writable(new Search());

export const storageKey = uuidv5(window.location.hostname, uuidv5.DNS);

export const showFilter = writable(false), showResults = writable(false);

export const tabIndex = writable(0), garageIndex = writable(0);

window.onbeforeunload = async function() {

    const indexes = {};

    tabIndex.update(state => {
        indexes.tab = state;
        return state;
    });

    currUser.update(state => {
        indexes.user = state;
        return state;
    });

    sessionStorage.setItem('idx', JSON.stringify(indexes));

    const cache = await caches.open('autoknct');
    await cache.delete('/bundle.js');
    await cache.delete('/bundle.css');
}

let inactivityTime = function () {
    let time;
    window.onload = resetTimer;
    // DOM Events
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
    document.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onmousedown = resetTimer; // touchscreen presses
    document.ontouchstart = resetTimer;
    document.onclick = resetTimer;     // touchpad clicks
    document.onscroll = resetTimer;    // scrolling with arrow keys
    document.onkeypress = resetTimer;

    function logout() {
        userExit();
    }

    function resetTimer() {
        clearTimeout(time);
        time = setTimeout(logout, 900000);
    }
};

window.onload = async function() {
    if (sessionStorage.getItem('idx') != null && sessionStorage.getItem(storageKey) != null) {

        const indexes = await JSON.parse(sessionStorage.getItem('idx'));
        
        await tabIndex.set(indexes.tab);

        await userInit(indexes.user.user_id, indexes.user, null);

        sessionStorage.removeItem('idx');
    }
    
    inactivityTime(); 
    const cache = await caches.open('autoknct');
    await cache.addAll(['/bundle.js', '/bundle.css']);
}