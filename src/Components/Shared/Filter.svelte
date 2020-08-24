<script>
    import { sortResults, queryResults, filterResults } from './../../Scripts/Filter.js';
    //import { tabIndex, showFilter } from './../../Scripts/states.js';
    import { tabIndex, showFilter } from './../../Scripts/Init.js';
    import { fly } from 'svelte/transition';
    import Card from './Template.svelte';

    export let results, prevResults, placeholder, filter;

    let userInput = '';

    let range = 10;

    let cylList = ['A', 'CC', 'S', 'None'];

    let statusList = ['Salvageable', 'Normal', 'Irreparable', 'Writeoff (Hail)', 'Writeoff (Stolen)', 'Writeoff (Other)', 'Rebuilt'];

    let propList = ['Model', 'Year', 'Date', 'Bid', 'Mileage'];

    var currDate = new window.Date();

    let yearList = [];

    let filters = {
        startYear : '', endYear : '',
        CYL : '',
        Status : '',
        startDate : '', endDate : '',
        minMile : '', maxMile : '',
        minBid : '', maxBid : ''
    }

    let sort, order;

    for(let i = currDate.getFullYear() + 1; i >= currDate.getFullYear() - 25; i--) 
        yearList.push(i);

    function clearFields() {
        filters.startYear = ''; filters.endYear = ''; 
        filters.CYL = ''; filters.Status = ''; 
        filters.startDate = ''; filters.maxBid;
        filters.minBid = ''; filters.maxBid = ''; 
        filters.minMile = ''; filters.maxMile = '';

        results = prevResults;
    }

    function goTop() {
        document.body.scrollTop = 0; 
        document.documentElement.scrollTop = 0;
    }
</script>

{#if prevResults.length > 10}
    <input id="search-bar" class="form-control-lg" placeholder="{placeholder}" bind:value="{userInput}" autocomplete="off" on:keyup="{() => results = queryResults(userInput, results, prevResults)}"/>

    <button id="filter" class="btn btn-info btn-lg" on:click="{() => showFilter.set(true)}"><i class="fa fa-filter"></i> Fliter {filter}</button>

    <button id="filter-mob" class="btn btn-info btn-lg" on:click="{() => showFilter.set(true)}"><i class="fa fa-filter"></i></button>

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

<div style="width:100%;margin-top:40px;">
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
</div>

<table style="width:100%">
    <tr>
        <td></td>
    </tr>
</table>

{#if range <= results.length && results.length > 0}
    <button id="loadMore" class="btn btn-primary" on:click="{() => range += 100}">Load More</button>
{/if}

{#if $showFilter}
    <div id="filterblock" class="container-fluid" in:fly="{{ x:200, duration:500 }}" out:fly="{{ x:200, duration:500 }}">
        <select class="form-control filterInput" aria-placeholder="CYL" bind:value="{filters.CYL}" on:change="{() => results = filterResults(filters, results)}">
            <option value="" disabled selected>CYL</option>
            {#each cylList as cyl}
                <option value="{cyl}">{cyl}</option>
            {/each}
        </select>

        <select class="form-control filterInput" bind:value="{filters.Status}" on:change="{() => results = filterResults(filters, results)}">
            <option value="" disabled selected>Status</option>
            {#each statusList as status}
                <option value="{status}">{status}</option>
            {/each}
        </select>

        <select class="form-control leftFilter" bind:value="{filters.startYear}" on:change="{() => results = filterResults(filters, results)}">
            <option value="" disabled selected>Start Year</option>
            {#each yearList as year}
                <option value="{year}">{year}</option>
            {/each}
        </select>

        <select class="form-control rightFilter" bind:value="{filters.endYear}" on:change="{() => results = filterResults(filters, results)}">
            <option value="" disabled selected>End Year</option>
            {#each yearList as year}
                <option value="{year}">{year}</option>
            {/each}
        </select>

        {#if $tabIndex != 0}
            <input class="form-control leftFilter" onfocus="this.type='Date'" placeholder="Start Date" autocomplete="off" bind:value="{filters.startDate}" on:change="{() => results = filterResults(filters, results)}"/>
            <input class="form-control rightFilter" onfocus="this.type='Date'" placeholder="End Date" autocomplete="off" bind:value="{filters.endDate}" on:change="{() => results = filterResults(filters, results)}"/>
        {/if}
        
        <input type="number" class="form-control leftFilter" placeholder="Min Mileage" autocomplete="off" bind:value="{filters.minMile}" on:keyup="{() => results = filterResults(filters, results)}"/>
        <input type="number" class="form-control rightFilter" placeholder="Max Mileage" autocomplete="off" bind:value="{filters.maxMile}" on:keyup="{() => results = filterResults(filters, results)}"/>
        <input type="number" class="form-control leftFilter" placeholder="Min Bid" autocomplete="off" bind:value="{filters.minBid}" on:keyup="{() => results = filterResults(filters, results)}"/>
        <input type="number" class="form-control rightFilter" placeholder="Max Bid" autocomplete="off" bind:value="{filters.maxBid}" on:keyup="{() => results = filterResults(filters, results)}"/>
        <button style="margin-top:10px;margin-bottom:10px;float:left;" class="btn btn-warning" on:click="{clearFields}">Reset</button>
        <button style="margin-top:10px;margin-bottom:10px;float:right;" class="btn btn-danger" on:click="{() => showFilter.set(false)}">Close</button>
    </div>
{/if}

<style>

    #search-bar {
        border-radius:0.4rem;
        outline:none;
        border:none;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        width:60%;
        -webkit-box-shadow:  0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    #filter {
        float: right;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-right: 20px;
    }

    #filter-mob {
        display:none;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        float:right;
        height:110px;
    }

    .sort {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-left:15px;
    }

    #goTop {
        z-index: 1;
        position: fixed;
        right: 20px;
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

    #loadMore {
        width:20%;
        margin-left:40%;
        margin-top:15px;
        margin-bottom:30px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    @media screen and (max-width:1024px) {

        #filter {
            display:none;
        }

        #search-bar {
            width:90%;
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

    @media screen and (max-width:720px) {

        #search-bar {
            width:100%;
        }

        #filter-mob {
            display:block;
            margin-top:10px;
        }

        #goTop {
            bottom: 60px;
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