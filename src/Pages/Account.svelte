<script>
    import Auser from './../Components/Account/Auser.svelte'
    import Buser from './../Components/Account/Buser.svelte';
    import Cuser from './../Components/Account/Cuser.svelte';
    //import { acctTab, storageKey, updateGarage, updateUser, invokeLambda } from './../Scripts/states.js';
    import { currUser, storageKey } from './../Scripts/Init.js';
    import { invokeLambda } from './../Scripts/Lambda.js';
    import { onMount } from 'svelte';
    import env from './../env.json';
</script>

<h1>Account</h1>

{#if $currUser.Type == null}
    <div class="text-center">
        <img src="https://autoarch.blob.core.windows.net/resources/loader.gif" alt="Loader"/>
    </div>
    <h6 style="text-align:center;">Loading...</h6>
{:else}
    {#if $currUser.Type[0] == 'A'}
        <Auser/>
    {:else if $currUser.Type[0] == 'B'}
        <Buser/>
    {:else}
        <Cuser/>
    {/if}
{/if}