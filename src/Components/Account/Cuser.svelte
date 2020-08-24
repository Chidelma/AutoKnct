<script>
    //import { resetStates, updateUser } from './../../Scripts/states.js';
    import { invokeLambda } from './../../Scripts/Lambda.js';
    import { currUser } from './../../Scripts/Init.js';
    import { userExit } from './../../Scripts/Entry.js';
    import { fly } from 'svelte/transition';
    import Modal from './../Shared/Modal.svelte';
    import Message from './../Shared/statusMsg.svelte';
    import env from './../../env.json';

    let Name = $currUser.Name;
    let Email = $currUser.Email;
    let Picture = $currUser.Picture;

    let mfaCode = '';

    let Payload, password, imageLabel = 'Choose Photo (<1MB)';

    let promptPassword = false, edit = false, del = false, mfa = true;
    
    let oldPassword = '', newPassword = '';

    let showMsg = false, statusColor = '', heading = '', message = ''; 

    document.documentElement.style.setProperty('--msg-color', statusColor);

    function upload(e) {
        if(e.target.files[0].size <= 1000000 && e.target.files[0].type == 'image/jpeg') {

            var reader = new FileReader();

            reader.onload = function (e) {
                Picture = e.target.result;
                acctTab.update(state => {
                    state.picture = e.target.result;
                    return state;
                });
            }

            reader.readAsDataURL(e.target.files[0]);
            imageLabel = e.target.files[0].name;

        } else if (e.target.files[0].size > 1000000 && e.target.files[0].type == 'image/jpeg') {
            showMsg = true, heading = 'Error - Profile Picture', message = "Image Larger than 1MB", statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);
        } else if (e.target.files[0].type != 'image/jpeg' && e.target.files[0].size <= 1000000 ) {
            showMsg = true, heading = 'Error - Profile Picture', message = "Image Is Not JPEG Format", statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);
        } else {
            showMsg = true, heading = 'Error - Profile Picture', message = "Image Is Not JPEG Format and Larger than 1MB", statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);
        }
    } 

    function editProfile() {

        if(Name != '' && Email != '' && password != '') {

            promptPassword = false;

            edit = false; del = false;

            Payload = {
                func : 'updateUser',
                username : $currUser.Username,
                password : password,
                name : Name,
                email : Email
            };

            invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                password = '';

                Payload = {
                    func : 'updateUser',
                    id : $currUser.user_id,
                    email : Email,
                    name : Name,
                    picture : Picture != null ? Picture : null
                };

                invokeLambda(env.lambda.pythonAPI, Payload).then(async (response) => {

                    if(response.includes('SUCCESS')) {

                        imageLabel = 'Choose Photo (<1MB)';

                        await currUser.update(state => {
                            state.Email = Email;
                            state.Name = Name;
                            return state;
                        });

                        showMsg = true, heading = 'SUCCESS!', message = 'Profile Updated', statusColor = 'green'; 

                        setTimeout(function(){ 
                            showMsg = false, heading = '', message = '', statusColor = ''; 
                        }, 2000);

                    } else {

                        showMsg = true, heading = 'Error - Profile', message = 'Unable To Update Profile', statusColor = 'red'; 

                        setTimeout(function(){ 
                            showMsg = false, heading = '', message = '', statusColor = ''; 
                        }, 2000);

                    }

                }).catch((err) => {
                    
                    showMsg = true, heading = 'Error - Profile', message = err, statusColor = 'red'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);

                });

            }).catch((err) => {

                showMsg = true, heading = 'Error - Profile', message = err, statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            });

        } else {

            showMsg = true, heading = 'Error - Profile', message = 'Please Fill Out All Fields', statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        }
    }

    function resetPassword() {

        if(oldPassword != '' && newPassword != '') {

            if(oldPassword != newPassword) {

                if(newPassword.length >= 8) {

                    Payload = {
                        func : 'resetPassword', 
                        username : $currUser.Username,
                        oldPassword : oldPassword,
                        newPassword : newPassword
                    };

                    invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                        if(response == 'SUCCESS') {

                            showMsg = true, heading = 'Success!', message = 'Password Changed', statusColor = 'green'; 

                            setTimeout(function() { 
                                showMsg = false, heading = '', message = '', statusColor = ''; 
                            }, 2000);

                            resetStates();

                        } else {

                            showMsg = true, heading = 'Failed!', message = 'Password Not Changed', statusColor = 'red'; 

                            setTimeout(function() { 
                                showMsg = false, heading = '', message = '', statusColor = ''; 
                            }, 2000);

                        }

                    }).catch((err) => {

                        showMsg = true, heading = 'Error - Profile', message = err, statusColor = 'red'; 

                        setTimeout(function(){ 
                            showMsg = false, heading = '', message = '', statusColor = ''; 
                        }, 2000);

                    });
                    
                }
                else {

                    showMsg = true, heading = 'Error - Profile', message = 'Password length has to be at least 8 characters', statusColor = 'red'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);

                }
            }
            else {

                showMsg = true, heading = 'Error - Profile', message = 'Old and New Password cannot be the same', statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            }
        }
        else {

            showMsg = true, heading = 'Error - Profile', message = "Please Fill Out Both Fields", statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        }
    }

    function confirmMFA() {

        if(mfaCode != '' && password != '') {

            Payload = {
                username : $currUser.Username,
                password : password,
                code : mfaCode,
                func : 'confirmMFA'
            }

            invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                password = '', mfaCode = '';

                console.log(response);

                if(response == 'SUCCESS') {

                    showMsg = true, heading = 'SUCCESS', message = "MFA Setup Successfully", statusColor = 'green'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);

                } else {
                    showMsg = true, heading = 'FAILED', message = "MFA Setup Failed", statusColor = 'red'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);
                }
                
            }).catch((err) => {

                console.log(err);

                showMsg = true, heading = 'Error', message = "Please Try Again Later", statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            });

        }
        else {

            showMsg = true, heading = 'Error - Sign In', message = "Please Fill All Fields!", statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        }
    }

    let screenWidth = screen.width;
</script>

{#if showMsg}
    <div id="status" class="container-fluid" in:fly="{{ x:200, duration:500 }}" out:fly="{{ x:200, duration:500 }}">
        <Message heading={heading} message={message} status={statusColor} />
    </div>
{/if}

{#if promptPassword}
    <Modal/>
    <div id="modal-content" class="container-fluid" in:fly="{{ y:-200, duration:500 }}" out:fly="{{ y:-200, duration:500 }}">
        <h6 style="text-align:center;margin-top:20px;">Please Type Password</h6>
        <input id="prompt" type="password" class="form-control" placeholder="Password" bind:value="{password}"/>
        <button style="float:left" class="btn btn-danger modalBtn" on:click="{() => { promptPassword = false; edit = false; del = false; }}">Cancel</button>
        {#if edit}
            <button class="btn btn-primary modalBtn" on:click="{editProfile}">Save</button>
        {:else}
            <button class="btn btn-primary modalBtn" on:click="{confirmMFA}">Verify</button>
        {/if}
    </div>
{/if}

<div id="settings">

<table class="acctTab" cellpadding='10'>
    <tr>
        <td>
            <h3>Edit Profile</h3>

            <div class="custom-file input-group" style="margin-top:20px;width:72.5%;float:right;">
                <input type="file" accept="image/jpeg" class="custom-file-input" id="customFile" on:change="{upload}">
                <label class="custom-file-label" for="customFile">{imageLabel}</label>
            </div>

            <div id="pic">
                {#if Picture == null}
                    <img alt="picture" src={'https://source.unsplash.com/900x900/?automobile'} style="width:85px;height:85px;border-radius:0.4rem;outline:none;" />
                {:else}
                    <img alt="picture" src={Picture} style="width:85px;height:85px;border-radius:0.4rem;outline:none;" />
                {/if}
            </div>

            <div class="input-group mb-2">
                <div class="input-group-prepend">
                    <div class="input-group-text">Name:</div>
                </div>
                <input type="text" class="form-control" id="inlineFormInputGroup" placeholder="{Name}" bind:value="{Name}">
            </div>

            <div class="input-group mb-2" style="margin-top:20px;">
                <div class="input-group-prepend">
                    <div class="input-group-text">Email:</div>
                </div>
                <input type="text" class="form-control" id="inlineFormInputGroup" placeholder="{Email}" bind:value="{Email}">
            </div>

            <button id="saveBtn" class="btn btn-primary" style="margin-top:20px;float:right" on:click="{() => { promptPassword = true; edit = true; }}"><i class="fa fa-save"></i> Save Changes</button>
        </td>
    </tr>
</table>

<table class="acctTab" cellpadding='10' style="margin-top:50px;">
    <tr>
        <td>
            <h3>Reset Password</h3>

            <input type="password" class="form-control reset"  placeholder="Old Password" bind:value="{oldPassword}">

            <input type="password" class="form-control reset"  placeholder="New Password" bind:value="{newPassword}">

            <button class="btn btn-primary" on:click="{resetPassword}" style="float:right;"><i class="fa fa-refresh"></i> Reset</button>
        </td>
    </tr>
</table>

</div>

<style>

    #settings {
        width:90%;
        height:100%;
        margin-top:20px;
    }

    .acctTab {
        width:33.33%;
    }

    #pic {
        width:85px;
        height:85px;
        background-color:grey;
        border-radius:0.4rem;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        float:left;
        margin-bottom:20px;
    }

    .reset {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
        margin-bottom:20px;
    }

    .input-group, .btn {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
    }

    #modal-content {
        z-index:123;
        width:20%;
        position:fixed;
        margin-left:38%;
        margin-top:1%;
        background-color:#7c7c7c;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
    }

    .modalBtn {
        margin-top:20px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-bottom:20px;
        float:right;
    }

    #prompt {
        margin-top:20px;
        background:black;
        border-radius:0.4rem;
        border:none;
        outline:none;
    }

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

    @media screen and (max-width: 1024px) {

        #settings {
            width:100%;
        }

        #status {
            width:80%;
            right: 10%;
        }

        .acctTab {
            width:100%;
        }

    }
</style>