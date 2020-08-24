<script>
    //import { acctTab, garageTab } from './../../Scripts/states.js';
    import { currUser } from './../../Scripts/Init.js';
    import Card from './../Shared/Template.svelte';
    import { onMount } from 'svelte';

    let results = $currUser.compare;

    setInterval(function() {
        results = $currUser.compare;
    }, 1000);
    
</script>


{#if results.length > 0}
    <div style="margin-top:10%;margin-left:40px;">
        <table style="float:left;font-size:13px;margin-top:123px;" width="140" height="211" border="0">
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="makeKey">Make</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="yearKey">Year</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="vinKey">Vin</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="cylKey">Cyl</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="statusKey">Status</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="mileKey">Mileage</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="dateKey">Auction Date</span>
                </td>
            </tr>
            <tr style="border-bottom:1px solid black;font-weight:bold;">
                <td align="center">
                    <span id="bidKey">Final Bid</span>
                </td>
            </tr>
        </table>

        {#each results as auto}
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
{:else}
    <h5 id="noneOwn">There Are No Vehicles Here For Comparsion</h5>
    <h5 style="text-align:center;">You Can Compare Up To 7 Vehicles</h5>
{/if}


<style>
    #noneOwn {
        text-align:center;
        margin-top:25%;
    }
</style>