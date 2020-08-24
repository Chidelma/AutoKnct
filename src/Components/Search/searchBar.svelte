<script>
    import { fly } from 'svelte/transition';
    import Card from './../Shared/Template.svelte';
    import Chart from './Chart.svelte';
    //import { searchTab, invokeLambda, acctTab, showResults } from './../../Scripts/states.js';
    import { currUser, searchTab, showResults } from './../../Scripts/Init.js';
    import { invokeLambda } from './../../Scripts/Lambda.js';
    import { sortResults } from './../../Scripts/Filter.js';
    import env from './../../env.json';

    let showFilter = false;

    let userInput = '';

    let results = [], prevResults = [];

    let xAxis, leftYAxis, rightYAxis;

    let xAxisPrev, leftYAxisPrev, rightYAxisPrev;

    let screenWidth = screen.width;

    let range = 100;

    let count = 0;

    let showMsg = false, statusColor = '', heading = '', message = ''; 

    let filters = {
        startYear : '', endYear : '',
        CYL : '',
        Status : '',
        startDate : '', endDate : '',
        minMile : '', maxMile : '',
        minBid : '', maxBid : ''
    }

    let sort, order;

    let userSearch = localStorage.getItem($currUser.user_id) != null ? JSON.parse(localStorage.getItem($currUser.user_id)).reverse() : [];

    if($searchTab.saved == true && $searchTab.results.length > 0) {

        count = $searchTab.results.length;

        document.documentElement.style.setProperty('--input-xpos', '0%');
        document.documentElement.style.setProperty('--input-ypos', '0%');

        userInput = $searchTab.userInput;

        results = $searchTab.results; 

        prevResults = $searchTab.prevResults;

        filters = $searchTab.filter;

        sort = $searchTab.sort;

        order = $searchTab.order;

        xAxis = $searchTab.xValues; xAxisPrev = $searchTab.xValuesPrev;

        leftYAxis = $searchTab.leftYValues; leftYAxisPrev = $searchTab.leftYValuesPrev;

        rightYAxis = $searchTab.rightYValues; rightYAxisPrev = $searchTab.rightYValuesPrev;
    }
    else {
        {document.documentElement.style.setProperty('--input-xpos', '20%')};
        {document.documentElement.style.setProperty('--input-ypos', '22%')};
    }

    let queryStatus = 'Loading';

    let cylList = ['A', 'CC', 'S', 'None'];

    let statusList = ['Salvageable', 'Normal', 'Irreparable', 'Writeoff (Hail)', 'Writeoff (Stolen)', 'Writeoff (Other)', 'Rebuilt'];

    let propList = ['Model', 'Year', 'Date', 'Bid', 'Mileage'];

    var currDate = new window.Date();

    let yearList = [];

    for(let i = currDate.getFullYear() + 1; i >= currDate.getFullYear() - 25; i--) 
        yearList.push(i);

    function searchHistory(term) {
        userInput = term;
        getResults();
        document.getElementById('search-mid').style.setProperty('--input-xpos', '0%');
        document.getElementById('search-mid').style.setProperty('--input-ypos', '0%');
        showResults.set(true);
    }

    async function checkChar() {

        count = 0;

        document.getElementById('search-mid').style.setProperty('--input-xpos', '0%');
        document.getElementById('search-mid').style.setProperty('--input-ypos', '0%');

        await getResults();

        showResults.set(true);

        let searchLog = await JSON.parse(localStorage.getItem($currUser.user_id));

        if(searchLog.length > 0) {

            let found = false;

            for(let i = 0; i < searchLog.length; i++) {
                if(searchLog[i] == userInput || searchLog[i].includes(userInput)) {
                    found = true;
                    break;
                } 
            }

            if(found == false){
                searchLog.push(userInput);
                await localStorage.setItem($currUser.user_id, JSON.stringify(searchLog));
            }
        }
        else {
            searchLog.push(userInput);
            await localStorage.setItem($currUser.user_id, JSON.stringify(searchLog));
        }
    }

    function getResults() {

        clearFields();

        let Payload = {
            func : 'searchQuery', 
            query : userInput.toUpperCase()
        };

        invokeLambda(env.lambda.pythonAPI, Payload).then(async (response) => {

            console.log(response);

            if(response.Results.length == 0) {
                queryStatus = 'No Results';
            } else {

                await searchTab.update(state => {
                    state.saved = true;
                    state.resultInit(response.Results);
                    state.userInput = userInput;
                    state.xValues = response.Dates; state.xValuesPrev = response.Dates;
                    state.leftYValues = response.Prices; state.leftYValuesPrev = response.Prices;
                    state.rightYValues = response.Counts; state.rightYValuesPrev = response.Counts;
                    return state;
                });

                console.log($searchTab.results);

                results = $searchTab.results;
                prevResults = $searchTab.results;
                xAxis = $searchTab.xValuesPrev; xAxisPrev = $searchTab.xValuesPrev;
                leftYAxis = $searchTab.leftYValues; leftYAxisPrev = $searchTab.leftYValuesPrev;
                rightYAxis = $searchTab.rightYValues; rightYAxisPrev = $searchTab.rightYValuesPrev;
                count = results.length;
            }

        }).catch((err) => {

            showMsg = true, heading = 'Error', message = err, statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 5000);

        });
    }

    function filterResults() {

        count = 0;

        let Payload = {
            func : 'filterResult', 
            filter : filters,
            result : results
        };

        invokeLambda(env.lambda.pythonAPI, Payload).then(async (response) => {

            if(response.Results.length == 0) {
                queryStatus = 'No Results';
            }
            else {

                await searchTab.update(state => {
                    state.saved = true;
                    state.results = response.Results;
                    state.xValues = response.Dates;
                    state.leftYValues = response.Prices;
                    state.rightYValues = response.Counts;
                    state.filter = filters;
                    return state;
                });

                results = $searchTab.results;
                xAxis = $searchTab.xValues;
                leftYAxis = $searchTab.leftYValues;
                rightYAxis = $searchTab.rightYValues;

                count = results.length; 
            }

        }).catch((err) => {

            showMsg = true, heading = 'Error', message = err, statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 5000);

        });
    }

    async function clearFields() {

        count = 0;

        filters.startYear = ''; filters.endYear = ''; 
        filters.CYL = ''; filters.Status = ''; 
        filters.startDate = ''; filters.maxBid;
        filters.minBid = ''; filters.maxBid = ''; 
        filters.minMile = ''; filters.maxMile = '';

        await searchTab.update(state => {
            state.results = prevResults;
            state.filter = filters;
            state.xValues = xAxisPrev;
            state.leftYValues = leftYAxisPrev;
            state.rightYValues = rightYAxisPrev;
            return state;
        });

        xAxis = xAxisPrev;
        leftYAxis = leftYAxisPrev;
        rightYAxis = rightYAxisPrev;

        results = prevResults;
        count = prevResults.length;
    }

    function goTop() {
        document.body.scrollTop = 0; 
        document.documentElement.scrollTop = 0;
    }

    let searchLog;
</script>

<input list="hist" id="search-mid" class="form-control-lg" placeholder="Search Model e.g Toyota Corolla" autocomplete="off" bind:value="{userInput}" on:keyup="{event => event.which == 13 && checkChar()}"/>
{#if userSearch.length > 0 && $showResults == false}
    <datalist id="hist">
        {#each userSearch.slice(0, 8) as hist}
            <option value="{hist}">{hist}</option>
        {/each}
    </datalist>
{/if}

{#if $showResults}
    {#if count == 0 && userInput.length > 0}
        {#if queryStatus == 'Loading'}
            <div class="text-center">
                <img src="https://autoarch.blob.core.windows.net/resources/loader.gif" alt="Loader"/>
            </div>
            <h5 style="text-align:center;">{queryStatus}</h5>
        {:else if queryStatus == 'No Results'}
            <h5 style="text-align:center;margin-top:40px;">{queryStatus}</h5>
        {/if}
    {:else if count > 0}
        {#if count > 10}
            <button id="filter" class="btn btn-info btn-lg" on:click="{() => showFilter = true}"><i class="fa fa-filter"></i> Fliter Results</button>
            
            <button id="filter-mob" class="btn btn-info btn-lg" on:click="{() => showFilter = true}"><i class="fa fa-filter"></i></button>

            <select class="form-control-lg sort" bind:value="{sort}" on:change="{() => results = sortResults(sort, order, results)}">
                {#each propList as prop}
                    <option value="{prop}">{prop}</option>
                {/each}
            </select>

            <select class="form-control-lg sort" bind:value="{order}" on:change="{() => results = sortResults(sort, order, results)}">
                <option value="asc">Ascending</option>
                <option value="dsc">Descending</option>
            </select>

            <button id="goTop" class="btn btn-primary btn-lg" on:click={goTop}>Top</button>
        {/if}

        {#if count == 1}
            <h5 style="text-align:center;margin-top:20px;margin-bottom:20px;">{count} Result Found</h5>
        {:else}
            <h5 style="text-align:center;margin-top:20px;margin-bottom:20px;">{count} Results Found</h5>
        {/if}

        {#if screenWidth >= 1024}
            <div class="box-body" style="margin-top:20px;padding:0px 15px 0px 15px;margin-bottom:20px;">
                <div id="searchChart" class="chart-container">
                    <Chart xValues={xAxis} yValues={leftYAxis} rightYValues={rightYAxis}/>
                </div>
            </div>
        {/if}

        {#each results.slice(0, range) as auto}
            {#if auto.Images === undefined || auto.Images.length == 0}
                <Card id={auto._id || auto.id} year={auto.Year} model={auto.Model} url={"https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"} 
                    vin={auto.VIN} cyl={auto.CYL} status={auto.Status} 
                    price={auto.Price} mileage={auto.Mileage} date={auto.Date} images={undefined}/>
            {:else}
                <Card id={auto._id || auto.id} year={auto.Year} model={auto.Model} url={auto.Images[0]} 
                    vin={auto.VIN} cyl={auto.CYL} status={auto.Status} price={auto.Price}
                    mileage={auto.Mileage} date={auto.Date} images={auto.Images}/>
            {/if}
        {/each}

        <table style="width:100%">
            <tr>
                <td></td>
            </tr>
        </table>

        {#if range <= count && count > 0}
            <button id="loadMore" class="btn btn-primary" on:click="{() => range += 100}">Load More</button>
        {/if}
    {/if}

    {#if showFilter}
        <div id="filterblock" class="container-fluid" in:fly="{{ x:200, duration:500 }}" out:fly="{{ x:200, duration:500 }}">
        <button style="margin-top:10px;margin-bottom:10px;float:left;" class="btn btn-warning" on:click="{clearFields}">Reset</button>
            <button style="margin-top:10px;margin-bottom:10px;float:right;" class="btn btn-danger" on:click="{() => showFilter = false}">Close</button>
            <select class="form-control filterInput" aria-placeholder="CYL" bind:value="{filters.CYL}">
                <option value="" disabled selected>CYL</option>
                {#each cylList as cyl}
                    <option value="{cyl}">{cyl}</option>
                {/each}
            </select>

            <select class="form-control filterInput" bind:value="{filters.Status}">
                <option value="" disabled selected>Status</option>
                {#each statusList as status}
                    <option value="{status}">{status}</option>
                {/each}
            </select>

            <select class="form-control leftFilter" bind:value="{filters.startYear}">
                <option value="" disabled selected>Start Year</option>
                {#if filters.endYear != ''}
                    {#each yearList as year}
                        {#if filters.endYear >= year}
                            <option value="{year}">{year}</option>
                        {/if}
                    {/each}
                {:else}
                    {#each yearList as year}
                        <option value="{year}">{year}</option>
                    {/each}
                {/if}
            </select>

            <select class="form-control rightFilter" bind:value="{filters.endYear}">
                <option value="" disabled selected>End Year</option>
                {#if filters.startYear != ''}
                    {#each yearList as year}
                        {#if filters.startYear <= year}
                            <option value="{year}">{year}</option>
                        {/if}
                    {/each}
                {:else}
                    {#each yearList as year}
                        <option value="{year}">{year}</option>
                    {/each}
                {/if}
            </select>

            <input class="form-control leftFilter" onfocus="this.type='Date'" placeholder="Start Date" autocomplete="off" bind:value="{filters.startDate}"/>
            <input class="form-control rightFilter" onfocus="this.type='Date'" placeholder="End Date" autocomplete="off" bind:value="{filters.endDate}"/>
            <input type="number" class="form-control leftFilter" placeholder="Min Mileage" autocomplete="off" bind:value="{filters.minMile}"/>
            <input type="number" class="form-control rightFilter" placeholder="Max Mileage" autocomplete="off" bind:value="{filters.maxMile}"/>
            <input type="number" class="form-control leftFilter" placeholder="Min Bid" autocomplete="off" bind:value="{filters.minBid}"/>
            <input type="number" class="form-control rightFilter" placeholder="Max Bid" autocomplete="off" bind:value="{filters.maxBid}"/>
            <button style="margin-top:10px;margin-bottom:10px;width:50%;margin-left:25%;" class="btn btn-info" on:click="{filterResults}">Filter</button>
        </div>
    {/if}
{/if}

<style>
    #search-mid {
        border-radius:0.4rem;
        outline:none;
        border:none;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        -webkit-box-shadow:  0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        width:60%;
        margin-top: var(--input-xpos);
        margin-left: var(--input-ypos);
    }

    #loadMore {
        width:20%;
        margin-left:40%;
        margin-top:30px;
        margin-bottom:30px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    #filter {
        float: right;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .sort {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-left:15px;
    }

    #goTop {
        z-index: 1;
        position: fixed;
        right: 15px;
        bottom: 30px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    #filterblock {
        z-index: 1;
        position: fixed;
        top: 60px;
        right: 20px;
        width:400px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        background-color: #7c7c7c;
        border-radius:0.4rem;
    }

    .filterInput {
        margin-top:20px;
        background-color:black;
        color:white;
        outline: none;
        border:none;
    }

    .leftFilter {
        width:45%;
        float:left;
        margin-top:20px;
        background-color:black;
        color:white;
        outline:none;
        border:none;
    }

    .rightFilter {
        width:45%;
        float:right;
        margin-top:20px;
        background-color:black;
        color:white;
        outline:none;
        border:none;
    }

    .text-center {
        margin-top:20%;
    }

    #filter-mob {
        display:none;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        float:right;
        height:110px;
    }

    @media screen and (max-width: 1024px) {
        
        #filter {
            display:none;
        }

        #search-mid {
            width:90%;
            margin-left:0px;
            margin-top:0px;
        }

        #filter-mob {
            display:block;
        }

        #goTop {
            bottom: 80px;
            right: 10px;
        }

        .sort {
            margin-top:10px;
            width:44.9%;
            margin-left:0px;
        }

    }

    @media screen and (max-width: 720px) {
        
        #search-mid {
            width:100%;
        }
/*
        #searchLog {
            width:100%;
            margin-left:unset;
        }

        .hist {
            width:100%;
            margin-bottom:20px;
            margin-left:unset;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        }
*/
        #filter-mob {
            display:block;
            margin-top:10px;
        }

        #goTop {
            bottom: 80px;
            right: 10px;
        }

        .sort {
            margin-top:10px;
            width:85%;
            margin-left:0px;
        }

        #filterblock {
            right: 0;
            width:100%;
        }

        #loadMore {
            width:40%;
            margin-left:30%;
        }

    }
</style>