<script>
    //import { acctTab, invokeLambda, resetStates, updateUser } from './../../Scripts/states.js';
    import { invokeLambda } from './../../Scripts/Lambda.js';
    import { currUser } from './../../Scripts/Init.js';
    import { onMount } from 'svelte';
    import env from './../../env.json';
    import Modal from './../Shared/Modal.svelte';
    import Message from './../Shared/statusMsg.svelte';
    import { fly } from 'svelte/transition';

    let addUser = false;

    let Payload;

    let count = 0;

    let users = [], prevUsers = [];

    let catList = ['Administrator', 'Business', 'Customer', 'Supervisor'];

    let currCat = '', userInput = '';

    let showMsg = false, statusColor = '', heading = '', message = ''; 

    let firstName = '', midName = '', lastName = '', dob = '', email = '';

    function getUsers() {

        Payload = {
            func : 'getAllUsers'
        }

        invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

            users = response;
            prevUsers = response;

            count = response.length;

            acctTab.update(state => {
                state.users = response;
                return state;
            });

        }).catch((err) => {
            console.log(err);
        });
    }

    function disableUser(username, email, userType) {

        Payload = {
            func : 'disableUser',
            username : username,
            email : email,
            userType : userType
        }

        invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

            console.log(response);

            if(response == 'SUCCESS') {

                showMsg = true, heading = 'SUCCESS!', message = 'User Disabled', statusColor = 'green'; 

                getUsers();

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            } else {

                showMsg = true, heading = 'Error - Disabling User', message = response, statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            }

        }).catch((err) => {

            console.log(err);

            showMsg = true, heading = 'Error - Disabling User', message = err, statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        });
    }

    function deleteUser(username, email, userType) {

        Payload = {
            func : 'deleteUser',
            username : username,
            email : email,
            userType : userType
        }

        invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

            console.log(response);

            if(response == 'SUCCESS') {

                showMsg = true, heading = 'SUCCESS!', message = 'User Deleted', statusColor = 'green'; 

                getUsers();

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            } else {

                showMsg = true, heading = 'Error - Disabling User', message = response, statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            }

        }).catch((err) => {

            console.log(err);

            showMsg = true, heading = 'Error - Disabling User', message = err, statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        });
    }

    function createUser() {

        if(firstName != '' && lastName != '' && dob != '' && currCat != '') {

            Payload = {
                func : 'createUser',
                user : $currUser.Username,
                firstName : firstName,
                midName : midName,
                lastName : lastName,
                dob : dob,
                group : currCat,
                email : email
            }

            invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

                console.log(response);

                if(response == 'SUCCESS') {

                    firstName = ''; lastName = ''; dob = ''; currCat = ''; midName = ''; email = ''; 

                    showMsg = true, heading = 'SUCCESS!', message = 'User Created', statusColor = 'green'; 

                    addUser = false;

                    getUsers();

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);

                } else {

                    showMsg = true, heading = 'Error - User Creation', message = response, statusColor = 'red'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);

                }

            }).catch((err) => {
                console.log(err);

                showMsg = true, heading = 'Error - User Creation', message = err, statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);
            });

        } else {
            showMsg = true, heading = 'Error - User Creation', message = 'Please Fill All Fields', statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);
        }
    }

    function searchUser() {

        let temp = [];

        for(let i = 0; i < users.length; i++) {
            if(users[i].Name.includes(userInput) || users[i].Email.includes(userInput) || users[i].Username.includes(userInput))
                temp.push(users[i]);
        }

        users = temp;
    }

    function filterUsers() {
        users = prevUsers;

        let temp = [];

        for(let i = 0; i < users.length; i++) {
            if(users[i].Type[0] == currCat[0])
                temp.push(users[i]);
        }

        users = temp;
    }

    function resetUsers() {
        users = prevUsers;
        userInput = '';
    }

    onMount(async () => {
        if($currUser.users == [] || typeof $currUser.users == "undefined") {
            await getUsers();
        } else {
            users = $currUser.users;
            prevUsers = $currUser.users;

            count = $currUser.users.length;
        }
    });
</script>

{#if showMsg}
    <div id="status" class="container-fluid" in:fly="{{ x:200, duration:500 }}" out:fly="{{ x:200, duration:500 }}">
        <Message heading={heading} message={message} status={statusColor} />
    </div>
{/if}

{#if addUser}
    <div style="float:right;">
        <h3 style="text-align:center;margin-top:10px;">Add User</h3>

        <input class="userform form-control" placeholder="First Name" bind:value="{firstName}"/>
        <input class="userform form-control" placeholder="Middle Name" bind:value="{midName}"/>
        <input class="userform form-control" placeholder="Last Name" bind:value="{lastName}"/>
        
        <input onfocus="this.type='Date'" class="userform form-control" placeholder="D.O.B." bind:value="{dob}"/>

        <select class="form-control userform" bind:value="{currCat}" on:change="{filterUsers}">
            <option value="" disabled selected>Category</option>
            {#each catList as cat}
                <option value="{cat}">{cat}</option>
            {/each}
        </select>

        {#if currCat[0] == 'C' || currCat[0] == 'B'}
            <input bind:value="{email}" class="userform form-control" placeholder="Email"/>
        {/if}

        <div style="width:100%;">
            <button style="margin-left:60px;width:25%;" class="btn btn-success" on:click="{createUser}">Add User <i class="fa fa-user-plus"></i></button>
        </div>
    </div>
{:else}
    {#if $currUser.Email == 'admin@autoknct.com'}
        <button style="float:right;margin-top:20px;" class="btn btn-primary" on:click="{() => addUser = true}">Add User <i class="fa fa-user-plus"></i></button>
    {:else}
        <button style="float:right;margin-top:20px;" class="btn btn-primary" on:click="{resetUsers}">Reset</button>
    {/if}

    <select class="form-control filterInput" bind:value="{currCat}" on:change="{filterUsers}">
        <option value="" disabled selected>Category</option>
        {#each catList as cat}
            <option value="{cat}">{cat}</option>
        {/each}
    </select>

    <input id="userSearch" class="form-control" placeholder="Search Users" bind:value="{userInput}" on:keyup="{searchUser}"/>

    {#if count == 0}
        <div class="text-center">
            <img src="https://autoarch.blob.core.windows.net/resources/loader.gif" alt="Loader"/>
        </div>
        <h6 style="text-align:center;">Loading...</h6>
    {:else}
        {#each users as user}
            <table cellpadding="10" class="user" width="90%" align="right" border="0">
                <tr>
                    <td align="center" width="100px">
                        <div id="pic">
                            {#if user.Picture == null}
                                <img alt="picture" src={'https://source.unsplash.com/900x900/?automobile'} style="width:85px;height:85px;border-radius:0.4rem;outline:none;" />
                            {:else}
                                <img alt="picture" src={user.Picture} style="width:85px;height:85px;border-radius:0.4rem;outline:none;" />
                            {/if}
                        </div>
                    </td>
                    <td>
                        <p>Name: <b>{user.Name}</b></p>
                        <p>Username: <b>{user.Username}</b></p>
                        <p>Email: <b>{user.Email}</b></p>
                    </td>
                    <td>
                        <p>Status: <b>{user.Status}</b></p>
                        {#if user.Type[0] == 'A'}
                            <p>Category: <b>Administrator</b></p>
                        {:else if user.Type[0] == 'B'}
                            <p>Category: <b>Business</b></p>
                        {:else}
                            <p>Category: <b>Customer</b></p>
                        {/if}
                        <p>Garage Count: <b>{user.Garage.Owned.length + user.Garage.Shared.length + user.Garage.Compare.length}</b></p>
                    </td>
                    <td width="25%">
                        {#if $currUser.user_id != user.id}
                            <button style="margin-bottom:10px;width:100%;" class="btn btn-success">Email User <i class="fa fa-envelope"></i></button>
                            {#if user.Type[0] != 'A'}
                                <button style="margin-bottom:10px;width:100%;" class="btn btn-warning" disabled="{!user.Enabled}" on:click="{() => disableUser(user.Username, user.Email, user.Type)}">Disable User <i class="fa fa-ban"></i></button>
                                <button style="width:100%;" class="btn btn-danger" on:click="{() => deleteUser(user.Username, user.Email, user.Type)}">Delete User <i class="fa fa-user-times"></i></button>
                            {:else if user.Type[0] == 'A' && $currUser.Email == 'admin@autoknct.com'}
                                <button style="margin-bottom:10px;width:100%;" class="btn btn-warning" disabled="{!user.Enabled}" on:click="{() => disableUser(user.Username, user.Email, user.Type)}">Disable User <i class="fa fa-ban"></i></button>
                                <button style="width:100%;" class="btn btn-danger" on:click="{() => deleteUser(user.Username, user.Email, user.Type)}">Delete User <i class="fa fa-user-times"></i></button>
                            {/if}
                        {/if}
                    </td>
                </tr>
            </table>
        {/each}
    {/if}
{/if}

<style>
    .user {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-bottom:20px;
        border-radius:0.4rem;
        background-color:#fff;
    }

    #pic {
        width:85px;
        height:85px;
        background-color:grey;
        border-radius:0.4rem;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .btn {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    #userSearch {
        border-radius:0.4rem;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-bottom:20px;
        margin-top:20px;
        width:60%;
        margin-left:10%;
    }

    .filterInput {
        width:15%;
        float:right;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
        margin-top:20px;
        margin-right:10px;
        
    }

    .userform {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-left:60px;
        margin-bottom:20px;
        width:25%;
        float:left;
    }
</style>