<script>
	import SideNav from './Components/Shared/SideNav.svelte';
	import Entry from './Components/Account/Entry.svelte';
	//import { tabIndex, acctTab, invokeLambda, storageKey, updateUser, updateGarage, resetStates, homeTab } from './Scripts/states.js';
	import Account from './Pages/Account.svelte';
	import Garage from './Pages/Garage.svelte';
	import Home from './Pages/Home.svelte';
	import Search from './Pages/Search.svelte';
	import { onMount } from 'svelte';
	import env from './env.json';
	import { currUser, tabIndex, homeTab, storageKey } from './Scripts/Init.js';
	import { userInit, userExit } from './Scripts/Entry.js';
	import { invokeLambda } from './Scripts/Lambda.js';

	let Name, Email, Picture, showUser = false;

	function initUser() {
		let UserID = sessionStorage.getItem(storageKey);

        let Payload = { 
            func : 'checkUser', 
            id : UserID
        };

        invokeLambda(env.lambda.pythonAPI, Payload).then(async (res) => {

			await userInit(res.user, res.id);

			Name = $currUser.Name;
			Email = $currUser.Email;
			Picture = $currUser.Picture;
/*
            updateUser(res.user, UserID); 
			updateGarage(res.garage);

			Name = $acctTab.name;
			Email = $acctTab.email;
			Picture = $acctTab.picture;
*/
			showUser = true;

        }).catch((err) => {
            console.log(err);
        });
	}

	setInterval(function() {
		Name = $currUser.Name;
		Email = $currUser.Email;
		Picture = $currUser.Picture;
/*
		Name = $acctTab.name;
		Email = $acctTab.email;
		Picture = $acctTab.picture;
*/
		showUser = true;
	}, 1000);

	onMount(async () => {

		if(sessionStorage.getItem(storageKey) != null && $currUser.isAuth) {
			await initUser();
		}
			
	});

</script>


{#if $currUser.isAuth == false && sessionStorage.getItem(storageKey) == null} 
	<Entry/>
{:else}
	<table align="center">
		<tr>
			<td>
				<img id="Logo" alt="Logo" src="{'https://autoarch.blob.core.windows.net/resources/LOGO.png'}"/>
			</td>
		</tr>
	</table>

	<SideNav/>

	{#if showUser}
		<table align="right" border="0">
			<tr>
				<td>
					<div id="pic">
						{#if Picture == null}
							<img alt="picture" src={'https://source.unsplash.com/900x900/?automobile'} style="width:40px;height:40px;border-radius:0.4rem;outline:none;" />
						{:else}
							<img alt="picture" src={Picture} style="width:40px;height:40px;border-radius:0.4rem;outline:none;" />
						{/if}
					</div>
				</td>
				<td>
					{#if Name !== undefined || Name != ''}
						<div class="dropdown">
							<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
								Hi {Name}!
							</button>
							<div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
								{#if $tabIndex != 3}
									<span class="dropdown-item" style="cursor:pointer;" on:click='{() => tabIndex.set(3)}'>Profile <i class="fa fa-user"></i></span>
								{/if}
								<span class="dropdown-item" style="cursor:pointer;" on:click='{userExit}'>Logout <i class="fa fa-sign-out"></i></span>
							</div>
						</div>
					{:else if typeof Name == undefined || Name == ''}
						<h6 id="salute">Hi User!</h6>
					{/if}
				</td>
			</tr>
		</table>
	{/if}

	{#if $tabIndex == 0}
		<div class="page">
			<Home/>
		</div>
	{:else if $tabIndex == 1}
		<div class="page">
			<Search/>
		</div>
	{:else if $tabIndex == 2}
		<div class="page">
			<Garage/>
		</div>
	{:else if $tabIndex == 3}
		<div class="page">
			<Account/>
		</div>
	{/if}
{/if}

<style>
	#pic {
        width:40px;
        height:40px;
        background-color:grey;
        border-radius:0.4rem;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

	#dropdownMenuButton {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
	}

	.dropdown-menu {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
	}

	.page {
		margin-left:5%;
		margin-right:5px;
		margin-top:5px;
		margin-bottom:5px;
	}

	#Logo {
		height:50px;
		position: absolute;
	}

	/* width */
	::-webkit-scrollbar {
		width: 10px;
	}

	/* Track */
	::-webkit-scrollbar-track {
		box-shadow: inset 0 0 5px grey; 
		border-radius: 10px;
	}
	
	/* Handle */
	::-webkit-scrollbar-thumb {
		background:#303030; 
		border-radius: 10px;
	}

	@media screen and (max-width:1024px) {

        .page {
			margin-left:0px;
			margin-right:0px;
			margin-top:0px;
			margin-bottom:0px;
		}

		#Logo {
			display:none;
		}
    }
</style>
