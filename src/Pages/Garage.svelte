<script>
    import Owned from './../Components/Garage/Owned.svelte';
    import Shared from './../Components/Garage/Shared.svelte';
    import Compare from './../Components/Garage/Compare.svelte';
    import { Tabs, Tab, TabList, TabPanel } from 'svelte-tabs';
    //import { garageIndex, garageTab } from './../Scripts/states.js';
    import { currUser, garageIndex } from  './../Scripts/Init.js' 

    let ownCount = $currUser.owned.length;
    let comCount = $currUser.compare.length;
    let shrCount = $currUser.shared.length;

    let screenWidth = screen.width;

    setInterval(function() {
        ownCount = $currUser.owned.length;
        comCount = $currUser.compare.length;
        shrCount = $currUser.shared.length;
    }, 1000);
</script>

<h1>Garage</h1>

<Tabs>
    <TabList>
        <Tab>
            <div on:click="{() => garageIndex.set(0)}">
                Owned
                {#if ownCount > 0}
                    <span class="badge badge-primary">{ownCount}</span>
                {/if}
            </div>
        </Tab>
        {#if screenWidth > 1024}
            <Tab>
                <div on:click="{() => garageIndex.set(1)}">
                    Compared
                    {#if comCount > 0}
                        <span class="badge badge-primary">{comCount}</span>
                    {/if}
                </div>
            </Tab>
        {/if}
        <Tab>
            <div on:click="{() => garageIndex.set(2)}">
                Shared
                {#if shrCount > 0}
                    <span class="badge badge-primary">{shrCount}</span>
                {/if}
            </div>
        </Tab>
    </TabList>

    <TabPanel>
        <Owned/>
    </TabPanel>

    {#if screenWidth > 1024}
        <TabPanel>
            <Compare/>
        </TabPanel>
    {/if}
    
    <TabPanel>
        <Shared/>
    </TabPanel>
</Tabs>

<style>
    .badge {
        z-index: 2;
        position:absolute;
    }
</style>