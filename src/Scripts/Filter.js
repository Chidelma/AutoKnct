//import { tabIndex, searchTab } from './states.js';
import { tabIndex, searchTab } from './Init';

export function queryResults(userInput, results, prevResults) {
    if(userInput.length > 0) {
        let tempResults = [];
    
        for(let i = 0; i < results.length; i++) {
            if(results[i].Model.includes(userInput.toUpperCase()))
                tempResults.push(results[i]);
        }

        if(tempResults.length == 0)
            return prevResults;
        else
            return tempResults;
    }
    if(userInput.length == 0) {
        return prevResults
    }
}

export function sortResults(sort, order, results) {
    if(order == 'asc') {
        if(sort == 'Model') {
            return results.sort(function(a, b) {
                let modelA = a.Model.toLowerCase(), modelB = b.Model.toLowerCase();

                if(modelA < modelB)
                    return -1;
                if(modelA > modelB)
                    return 1;
                return 0;
            });
        }
        else if(sort == 'Year'){
            return results.sort(function(a, b) {
                return a.Year - b.Year;
            });
        }
        else if(sort == 'Date') {
            return results.sort(function(a, b) {
                let dateA = new window.Date(a.Date), dateB = new window.Date(b.Date);
                return dateA - dateB;
            });
        }
        else if(sort == 'Bid') {
            return results.sort(function(a, b) {
                return a.Price - b.Price;
            });
        }
        else if(sort == 'Mileage') {
            return results.sort(function(a, b) {
                return a.Mileage - b.Mileage;
            });
        }
    }
    else if(order == 'dsc') {
        if(sort == 'Model') {
            return results.sort(function(a, b) {
                let modelA = a.Model.toLowerCase(), modelB = b.Model.toLowerCase();

                if(modelA > modelB)
                    return -1;
                if(modelA < modelB)
                    return 1;
                return 0;
            });
        }
        else if(sort == 'Year'){
            return results.sort(function(a, b) {
                return b.Year - a.Year;
            });
        }
        else if(sort == 'Date') {
            return results.sort(function(a, b) {
                let dateA = new window.Date(a.Date), dateB = new window.Date(b.Date);
                return dateB - dateA;
            });
        }
        else if(sort == 'Bid') {
            return results.sort(function(a, b) {
                return b.Price - a.Price;
            });
        }
        else if(sort == 'Mileage') {
            return results.sort(function(a, b) {
                return b.Mileage - a.Mileage;
            });
        }
    }

    let idx = null;

    tabIndex.update(state => {
        idx = state;
        return state;
    });

    if(idx == 1) {
        searchTab.update(state => {
            state.results = results;
            state.order = order;
            state.sort = sort;
            return state;
        });
    }
}

export function filterResults(auto, results) {
    let tempResults = [];

    if(auto.startYear != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Year >= auto.startYear) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.endYear != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Year <= auto.endYear) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.CYL != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].CYL.includes(auto.CYL) && results[i].CYL != null) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.Status != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Status == auto.Status) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.startDate != '') {
        let startDate = parseInt(auto.startDate.replace('-', '').replace('-', ''));
        for(let i = 0; i < results.length; i++) {
            let resultDate = parseInt(results[i].Date.replace('-', '').replace('-', ''));
            if(resultDate >= startDate) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.endDate != '') {
        let endDate = parseInt(filters.endDate.replace('-', '').replace('-', ''));
        for(let i = 0; i < results.length; i++) {
            let resultDate = parseInt(results[i].Date.replace('-', '').replace('-', ''));
            if(resultDate <= endDate) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.minMile != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Mileage >= auto.minMile) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.maxMile != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Mileage >= auto.maxMile) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.minBid != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Price >= auto.minBid) {
                tempResults.push(results[i]);
            }
        }
    }

    if(auto.maxBid != '') {
        for(let i = 0; i < results.length; i++) {
            if(results[i].Price <= auto.maxBid) {
                tempResults.push(results[i]);
            }
        }
    }

    if(tabIndex == 1) {
        searchTab.update(state => {
            state.results = tempResults;
            state.filter = auto;
            return state;
        });
    }

    return tempResults;
}

export function convertToCurrency(num) {
    return (num).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')
}