<script>
    //import { tabIndex, garageTab, showFilter } from './../../Scripts/states.js';
    import { tabIndex, currUser, showFilter } from './../../Scripts/Init.js';
    import { Tabs, Tab, TabList, TabPanel } from 'svelte-tabs';
    import Account from './../../Pages/Account.svelte';
	import Garage from './../../Pages/Garage.svelte';
	import Home from './../../Pages/Home.svelte';
	import Search from './../../Pages/Search.svelte';

    let count;

    setTimeout(function() {

        if(screen.width <= 1024) {
            count = $currUser.shared.length + $currUser.owned.length;
        }
        else {
            count = $currUser.compare.length + $currUser.shared.length + $currUser.owned.length;
        }
    }, 2000);

    setTimeout(function() {
        if($tabIndex == 0) {
            document.documentElement.style.setProperty('--home-color', '#ffc107');
            document.documentElement.style.setProperty('--search-color', '#fff');
            document.documentElement.style.setProperty('--garage-color', '#fff');
            document.documentElement.style.setProperty('--account-color', '#fff');
        }
        else if($tabIndex == 1) {
            document.documentElement.style.setProperty('--home-color', '#fff');
            document.documentElement.style.setProperty('--search-color', '#ffc107');
            document.documentElement.style.setProperty('--garage-color', '#fff');
            document.documentElement.style.setProperty('--account-color', '#fff');
        }
        else if($tabIndex == 2) {
            document.documentElement.style.setProperty('--home-color', '#fff');
            document.documentElement.style.setProperty('--search-color', '#fff');
            document.documentElement.style.setProperty('--garage-color', '#ffc107');
            document.documentElement.style.setProperty('--account-color', '#fff');
        }
        else {
            document.documentElement.style.setProperty('--home-color', '#fff');
            document.documentElement.style.setProperty('--search-color', '#fff');
            document.documentElement.style.setProperty('--garage-color', '#fff');
            document.documentElement.style.setProperty('--account-color', '#ffc107');
        }
    }, 1000);

    function changeIndex(idx) {
        showFilter.set(false);

        if(idx == 0) {
            tabIndex.set(idx);
            document.documentElement.style.setProperty('--home-color', '#ffc107');
            document.documentElement.style.setProperty('--search-color', '#fff');
            document.documentElement.style.setProperty('--garage-color', '#fff');
            document.documentElement.style.setProperty('--account-color', '#fff');
        }
        else if(idx == 1) {
            tabIndex.set(idx);
            document.documentElement.style.setProperty('--home-color', '#fff');
            document.documentElement.style.setProperty('--search-color', '#ffc107');
            document.documentElement.style.setProperty('--garage-color', '#fff');
            document.documentElement.style.setProperty('--account-color', '#fff');
        }
        else if(idx == 2) {
            tabIndex.set(idx);
            document.documentElement.style.setProperty('--home-color', '#fff');
            document.documentElement.style.setProperty('--search-color', '#fff');
            document.documentElement.style.setProperty('--garage-color', '#ffc107');
            document.documentElement.style.setProperty('--account-color', '#fff');
        }
        else {
            tabIndex.set(idx);
            document.documentElement.style.setProperty('--home-color', '#fff');
            document.documentElement.style.setProperty('--search-color', '#fff');
            document.documentElement.style.setProperty('--garage-color', '#fff');
            document.documentElement.style.setProperty('--account-color', '#ffc107');
        }
    }

    setInterval(function() {
        if(screen.width <= 1024) {
            count = $currUser.shared.length + $currUser.owned.length;
        }
        else {
            count = $currUser.compare.length + $currUser.shared.length + $currUser.owned.length;
        }
    }, 3000);

    let margin = 0.2 * screen.height;

    document.documentElement.style.setProperty('--top-margin', margin + 'px');

    let current = 'home';
</script>

<div id="sidebar-outer">
    <table id="sidebar-inner">
        <tr>
            <td class="tabIndex" align="center">
                <span style="color:#fff;;">Home</span>
                <i class="fa fa-home fa-3x" on:click="{() => changeIndex(0)}"></i>
            </td>
        </tr>
        <tr>
            <td class="tabIndex" align="center">
                <span style="color:#fff;">Search</span>
                <i class="fa fa-search" on:click="{() => changeIndex(1)}"></i>
            </td>
        </tr>
        <tr>
            <td class="tabIndex" align="center">
                <span style="color:#fff;">Garage</span>
                <i class="fa fa-car" on:click="{() => changeIndex(2)}">
                    {#if count > 0}
                        <span id="badgeCount" class="badge badge-primary">{count}</span>
                    {/if}
                </i>
            </td>
        </tr>
        <tr>
            <td class="tabIndex" align="center">
                <span style="color:#fff;">Account</span>
                <i class="fa fa-user fa-3x" on:click="{() => changeIndex(3)}"></i>
            </td>
        </tr>
    </table>
</div>

<div id="sidebar-outer-mob">
    <table id="sidebar-inner-mob" cellpadding="10">
        <tr height="50">
            <td class="tabIndex" align="center" on:click="{() => changeIndex(0)}">
                <i class="fa fa-home"></i>
            </td>
            <td class="tabIndex" align="center" on:click="{() => changeIndex(1)}">
                <i class="fa fa-search"></i>
            </td>
            <td class="tabIndex" align="center" on:click="{() => changeIndex(2)}">
                <i class="fa fa-car">
                    {#if count > 0}
                        <span id="badgeCount-mob" class="badge badge-primary">{count}</span>
                    {/if}
                </i>
            </td>
            <td class="tabIndex" align="center" on:click="{() => changeIndex(3)}">
                <i class="fa fa-user"></i>
            </td>
        </tr>
    </table>
</div>

<style>
    #badgeCount {
        z-index:1;
        position:fixed;
        font-size:15px;
        left:10px;
    }

    #badgeCount-mob {
        z-index:1;
        position:fixed;
        font-size:15px;
    }

    .tabIndex {
        cursor:pointer;
    }

    #sidebar-inner {
        width:100%;
        margin-top:var(--top-margin);
    }

    #sidebar-inner-mob {
        width:100%;
    }

    #sidebar-outer {
        width:60px;
        height: 98%;
        background-color:#303030;
        border-radius: 0.4rem;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        z-index:1;
        position: fixed;
    }

    #sidebar-outer-mob {
        width:101%;
        height: 65px;
        background-color:#303030;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        z-index:1;
        position: fixed;
        bottom:-10px;
        left:0;
        display:none;
    }

    .fa-user {
        color:var(--account-color);
    }

    .fa-home {
        color:var(--home-color);
    }

    .fa {
        margin-bottom:50px;
        text-align:center;
        cursor: pointer;
    }

    .fa-car {
        font-size:40px;
        color:var(--garage-color);
    }

    .fa-search {
        font-size:40px;
        color:var(--search-color);
    }

    @media screen and (max-width: 1024px) {
        
        #sidebar-outer {
            display:none;
        }

        #sidebar-outer-mob {
            display:block;
        }

        .fa-car {
            font-size:27px;
            color:var(--garage-color);
        }

        .fa-search {
            font-size:27px;
            color:var(--search-color);
        }

        .fa-user {
            font-size:27px;
            color:var(--account-color);
        }

        .fa-home {
            font-size:29px;
            color:var(--home-color);
        }

        #badgeCount-mob {
            font-size:10px;
        }

    }
</style>