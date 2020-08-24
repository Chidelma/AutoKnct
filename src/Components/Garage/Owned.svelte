<script>
    import { onMount } from 'svelte';
    //import { acctTab, garageTab } from './../../Scripts/states.js';
    import { currUser } from './../../Scripts/Init.js';
    import Filter from './../Shared/Filter.svelte';

    let results = $currUser.owned, prevResults = $currUser.owned;

    setInterval(function() {
        results = $currUser.owned;
        prevResults = $currUser.owned;
    }, 1000);
    
</script>

{#if results.length > 0}
    <Filter results={results} prevResults={prevResults} placeholder={'Search Garage'} filter={'Garage'}/>
{:else}
    <h5 id="noneOwn">There Are No Vehicles Here</h5>
{/if}

<style>
    #noneOwn {
        text-align:center;
        margin-top:25%;
    }
</style>