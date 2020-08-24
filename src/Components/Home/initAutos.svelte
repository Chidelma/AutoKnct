<script>
    import Card from './../Shared/Template.svelte';
    import { invokeLambda } from './../../Scripts/Lambda.js';
    import { fly } from 'svelte/transition';
    import Message from './../Shared/statusMsg.svelte';
    import Filter from './../Shared/Filter.svelte';
    import env from './../../env.json';
    import { onMount } from 'svelte';
    import { homeTab, storageKey, currUser } from './../../Scripts/Init.js';
    import { Home } from './../../Scripts/Home.js';

    let next = [];

    let showMsg = false, heading = '', message = '', statusColor = ''; 

    let screenWidth = screen.width;

    document.documentElement.style.setProperty('--msg-color', statusColor);

    if(sessionStorage.getItem(storageKey) == null) {

        sessionStorage.setItem(storageKey, $currUser.user_id);

        setTimeout(function() { 
            showMsg = true, heading = 'Successful Login!', message = 'Welcome ' + $currUser.Name, statusColor = 'green';
        }, 1000);

        setTimeout(function() { 
            showMsg = false, heading = '', message = '', statusColor = ''; 
        }, 3000);
    }

    function initHome() {

		let Payload = { func : 'initRecords' };

        invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

            //console.log(response);

            homeTab.update(state => {
                state.initHome(response);
                return state;
            });

            next = $homeTab.next;
        
        }).catch((err) => {

            console.log(err);

            showMsg = true, heading = 'Error - Home', message = 'Unable To Get Latest Updates', statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 5000);

        });
    }
    
    onMount(async () => {
        if($homeTab.saved) {
            next = await $homeTab.next;
        } else{
            await initHome();
        }
    });
</script>

{#if showMsg}
    <div id="status" class="container-fluid" in:fly="{{ x:200, duration:500 }}" out:fly="{{ x:200, duration:500 }}">
        <Message heading={heading} message={message} status={statusColor} />
    </div>
{/if}

{#if next.length == 0}
    <div class="text-center">
        <img src="https://autoarch.blob.core.windows.net/resources/loader.gif" alt="Loader"/>
    </div>
    <h6 style="text-align:center;">Loading...</h6>
{:else}
    <h2 id="heading">Upcoming Auctions</h2>

    <Filter results={next} prevResults={next} placeholder={'Search Upcoming Auctions'} filter={'Auction'}/>

    <table style="width:100%">
        <tr>
            <td></td>
        </tr>
    </table>

    {#if screenWidth <= 1024}
        <table style="width:100%;height:100px;">
            <tr>
                <td>
                </td>
            </tr>
        </table>
    {/if}
{/if}


<style>
    #status {
        z-index: 2;
        position: fixed;
        top: 20px;
        right: 20px;
        width:20%;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
        background-color: var(--msg-color);
    }

    #heading {
        margin-top:25px;
        margin-bottom:25px;
        text-align: center;
    }

    .text-center {
        margin-top:20%;
    }

    @media screen and (max-width: 1024px) {
        
        #heading {
            margin-top:10px;
        }

        #status {
            width:80%;
            right: 10%;
        }

    }
</style>

