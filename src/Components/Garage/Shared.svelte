<script>
    //import { acctTab, garageTab } from './../../Scripts/states.js';
    import { currUser } from './../../Scripts/Init.js';
    import Card from './../Shared/Template.svelte';
    import Filter from './../Shared/Filter.svelte';

    let results = $currUser.shared, prevResults = $currUser.shared;

    setInterval(function() {
        results = $currUser.shared;
        prevResults = $currUser.shared;
    }, 1000);

    let cars = [];
</script>

{#if results.length > 0}
    <Filter results={results} prevResults={prevResults} placeholder={'Search Shared Garage'} filter={'Garage'}/>
{:else}
    <h5 id="noneShare">There Are No Vehicles Here</h5>
{/if}

<style>
    #noneShare {
        text-align:center;
        margin-top:25%;
    }
</style>