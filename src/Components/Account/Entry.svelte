<script>
    import { invokeLambda } from './../../Scripts/Lambda.js';
    import { fly } from 'svelte/transition';
    import Modal from './../Shared/Modal.svelte';
    import Message from './../Shared/statusMsg.svelte';
    import ErrMsg from './ErrorMsg.svelte';
    import env from './../../env.json';
    import { currUser, storageKey } from './../../Scripts/Init.js';
    import { userInit } from './../../Scripts/Entry.js';

    let Payload, isAdmin = false;

    let signUpFlow = 0, signInFlow = 0;

    let logUsername = '', logPassword = '';

    let regName = '', regEmail = '', regUsername = '', regPassword  = '', regConPassword = '', regCode = '';

    let logLoading = false, regLoading = false;

    let showMsg = false, statusColor = '', heading = '', message = '', showRightMsg = false; 

    document.documentElement.style.setProperty('--msg-color', statusColor);

    function checkForAdmin() {
        if(logUsername.includes('autoknct.com')) {
            isAdmin = true;
        }
    }

    function checkUser() {

        if(logUsername != '') {

            logLoading = true;

            Payload = {
                username : logUsername.toLowerCase(),
                func : 'checkUser'
            }

            invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                if(response.CodeDeliveryDetails != undefined) {

                    showMsg = true, heading = 'SUCCESS!', message = 'Please Check Email (Spam) For Verification Code', statusColor = 'green'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 5000);

                    logLoading = false; signInFlow = 2;

                } else {

                    console.log(response);

                    showMsg = true, message = "Please Try Again Later"; 

                }
            }).catch((err) => {

                console.log(err);

                showMsg = true, message = "Please Try Again Later"; 

            });
        }
        else {
            showtMsg = true, message = "Please Fill Username"; 
        }
    }

    function resetPassword() {

        if(logUsername != '' && regCode != '' && logPassword != '') {

            logLoading = true;

            Payload = {
                username : logUsername.toLowerCase(),
                password : logPassword,
                code : regCode,
                func : 'confirmPassword'
            }

            invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                console.log(response);

                logUsername = '', logPassword = '', regCode = '';

                logLoading = false;

                if(response == null) {

                    showMsg = true, heading = 'SUCCESS!', message = 'Please Login With New Password', statusColor = 'green'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 5000);

                    signInFlow = 0;

                } else {

                    console.log(response);

                    showMsg = true, message = "Please Try Again Later"; 

                }

            }).catch((err) => {

                console.log(err);

                showMsg = true, message = "Please Try Again Later"; 

            });
        }
        else {
            showMsg = true, message = "Please Fill Out Fields"; 
        }
    }

    let currentUser;

    function resetEmailPassword(email, password) {

        Payload = {
            func : 'resetEmail', 
            email : email,
            newPassword : password
        };

        invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

            if(response == 'SUCCESS') {

                showMsg = true, heading = 'Success!', message = 'Password Changed', statusColor = 'green'; 

                setTimeout(function() { 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            } else {

                showMsg = true, message = 'Password Not Changed'; 

            }

        }).catch((err) => {

            showMsg = true, message = err; 

        });

    }

    function logIn() {

        if(logUsername != '' && logPassword != '') {

            logLoading = true;

            Payload = { 
                func : 'signIn', 
                username : logUsername.toLowerCase(),
                password : logPassword,
                newPassword : regPassword,
                code : regCode
            }

            invokeLambda(env.lambda.nodeAPI, Payload).then(async (response) => {

                await currUser.update(state => {
                    state.setKeyCode(response);
                    return state;
                });

                if(response.tokns != null) {

                    await currUser.update(state => {
                        state.setTokens(response);
                        return state;
                    });

                    initUser(response.tokns.idToken.payload);
                } else {

                    await currUser.update(state => {
                        state.setTokens(response);
                        return state;
                    });

                    initUser(response.idToken.payload);
                }

            }).catch((err) => {

                console.log(err);

                logLoading = false;

                showMsg = true, message = "The Username or Password you've entered is incorrect. Please try again.";

            });
        }
        else {

            showMsg = true, message = "Please Fill All Fields!";

        }
    }

    function initUser(response) {

        if(response.email_verified == "false") {

            signUpFlow = 1;

            logLoading = false;

            showRightMsg = true, message = 'Please Verify Your Email'; 

        } else {

            Payload = { 
                func : 'checkUser', 
                username : response['cognito:username'],
                name : response.name,
                email : response.email
            };

            invokeLambda(env.lambda.pythonAPI, Payload).then((res) => {

                //console.log(res);

                logUsername = '', logPassword = '', regCode = '';

                logLoading = false;

                userInit(res.id, res.user, res.garage);

                //console.log($currUser);
                
                if(regPassword != '' && response.email.includes('autoknct.com'))
                    resetEmailPassword(response.email, regPassword)

            }).catch((err) => {

                console.log(err);

                logLoading = false;

                showMsg = true, message = 'Problem Signing in. Please Try Again Later'; 

            });
        }
    }

    function register() {

        if(regEmail != '' && regName != '' && regUsername != '' && regPassword != '' && regConPassword != '') {

            if(regConPassword == regPassword) {

                regLoading = true;

                Payload = { 
                    func : 'signUp', 
                    username : regUsername.toLowerCase(),
                    password : regPassword,
                    name : regName,
                    email : regEmail,
                };

                invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                    console.log(response);

                    regLoading = false;

                    if(response.user != null) 
                        signUpFlow = 1;
                    else {

                        regLoading = false;

                        showRightMsg = true, message = "Please try Again"; 

                    }

                }).catch((err) => {

                    console.log(err);

                    regLoading = false;

                    showRightMsg = true, message = err; 

                });
            }
            else {

                regLoading = false;

                showRightMsg = true, message = "Passwords Do Not Match!"; 

            }
        }
        else {

            regLoading = false;

            showRightMsg = true, message = "Please Fill all Fields!"; 

        }
    }

    function resendCode() {

        Payload = { 
            func : 'confirmCode', 
            username : regUsername != '' ? regUsername.toLowerCase() : logUsername.toLowerCase(),
            resend : true
        };

        invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

            console.log(response);

            if(response.includes('resent')) {
                signUpFlow = 1;
            }
            else {
                showRightMsg = true, message = response; 
            }

        }).catch((err) => {

            showRightMsg = true, message = err; 

        });

    }

    function confirmCode() {

        if(regCode != '') {

            regLoading = true;

            Payload = { 
                func : 'confirmCode', 
                username : regUsername != '' ? regUsername.toLowerCase() : logUsername.toLowerCase(),
                resend : false,
                code : regCode
            };

            invokeLambda(env.lambda.nodeAPI, Payload).then((response) => {

                regLoading = false;

                if(response.includes("SUCCESS")) {

                    showMsg = true, heading = 'SUCCESS!', message = 'Registration Complete!', statusColor = 'green'; 

                    setTimeout(function(){ 
                        showMsg = false, heading = '', message = '', statusColor = ''; 
                    }, 2000);

                    if(screenWidth <= 1024) {
                        showSignIn = true; showSignUp = false;
                    }
                    else
                        signUpFlow = 2;
                }
                else {

                    showRightMsg = true, message = response; 

                }

            }).catch((err) => {

                showRightMsg = true, message = err; 

            });
        }
        else {

            regLoading = false;

            showRightMsg = true, message = "Please Fill all Fields!"; 

        }

    }

    let screenWidth = screen.width;

    let leftMargin = ((screen.width - 187) / 2) + 20;

    document.documentElement.style.setProperty('--left-Margin', leftMargin + 'px');

    let showSignUp = true, showSignIn = true;

    if(screenWidth < 1024) {
        showSignUp = false;
    }

    function externalSignIn(provider) {
        console.log(window.location.href);
        if(provider == 'FaceBook') {
            window.location.href = 'https://autoknct.auth.ca-central-1.amazoncognito.com/oauth2/authorize?identity_provider=Facebook&redirect_uri='+ window.location.href + '&response_type=token&client_id=hhj39244ktpq30gbq9ut6b84p&scope=email+openid+phone+profile';
        }
    }
</script>

<table align="center">
    <tr>
        <td>
            <img id="Logo" alt="Logo" src="{'https://autoarch.blob.core.windows.net/resources/LOGO.png'}"/>
        </td>
    </tr>
</table>

<Modal/>
{#if showSignIn}
    {#if signInFlow == 0}
        <div id="signIn" class="container-fluid">
            <h6 style="text-align:center;margin-top:-10px;">Sign Into Your Account</h6>
            {#if showMsg}
                <ErrMsg message={message} />
            {/if}
            <input bind:value="{logUsername}" class="form-control login" placeholder="username or email" autocomplete="off" on:keyup='{checkForAdmin}'/>
            <input type="password" bind:value="{logPassword}" class="form-control login" placeholder="password" autocomplete="off" on:keydown="{event => event.which === 13 && logIn()}"/>
            {#if isAdmin}
                <input bind:value="{regCode}" class="form-control login" placeholder="One-Time Passcode" autocomplete="off" on:keydown="{event => event.which === 13 && logIn()}"/>
            {/if}
            <button class="btn btn-success" on:click="{logIn}" disabled="{logLoading}">
                {#if logLoading}
                    <i class="fa fa-spinner fa-pulse"></i>
                {:else}
                    <i class="fa fa-sign-in"></i> Login
                {/if}
            </button>
            <p style="text-align:center;margin-top:20px;cursor:pointer;" on:click="{() => signInFlow = 1}">Forgot Password?</p>
            {#if screenWidth <= 1024}
                <p style="text-align:center;margin-top:20px;cursor:pointer;" on:click="{() => {showSignIn = false; showSignUp = true; }}">Don't Have an Account? <span style="color:blue;">Sign Up</span></p>
            {/if}

            <hr/>

            <button class="btn-primary btn" on:click='{() => externalSignIn('FaceBook')}' style="width:100%;margin-left:0;"><i class="fa fa-facebook-square"></i> Login in wIth Facebook</button>
            <button class="btn-danger btn" on:click='{() => externalSignIn('Google')}' style="width:100%;margin-left:0;"><i class="fa fa-google"></i> Login in wIth Google</button>
        </div>
    {:else if signInFlow == 1}
        <div id="signIn" class="container-fluid">
            <h6 style="text-align:center;">Please Fill Out Your Username or Email</h6>
            {#if showMsg}
                <ErrMsg message={message} />
            {/if}
            <input bind:value="{logUsername}" class="form-control login" placeholder="username or email" autocomplete="off" on:keyup='{checkForAdmin}' on:keydown="{event => event.which === 13 && checkUser()}"/>
            {#if isAdmin}
                <input type="password" bind:value="{logPassword}" class="form-control login" placeholder="Password" autocomplete="off"/>
                <input type="password" bind:value="{regPassword}" class="form-control login" placeholder="New Password" autocomplete="off" on:keydown="{event => event.which === 13 && logIn()}"/>
            {/if}
            <button class="btn btn-danger" style="float:left;margin-left:0px;width:30%;" on:click="{() => signInFlow = 0}">
                Back
            </button>
            {#if isAdmin}
                <button class="btn btn-success" style="float:right;width:30%;" on:click="{logIn}" disabled="{logLoading}">
                    {#if logLoading}
                        <i class="fa fa-spinner fa-pulse"></i>
                    {:else}
                        Reset
                    {/if}
                </button>
            {:else}
                <button class="btn btn-success" style="float:right;width:30%;" on:click="{checkUser}" disabled="{logLoading}">
                    {#if logLoading}
                        <i class="fa fa-spinner fa-pulse"></i>
                    {:else}
                        Next
                    {/if}
                </button>
            {/if}
        </div>
    {:else if signInFlow == 2}
        <div id="signIn" class="container-fluid">
            <h6 style="text-align:center;">Fill Out Verification Code and New Password</h6>
            {#if showMsg}
                <ErrMsg message={message} />
            {/if}
            <input bind:value="{regCode}" class="form-control login" placeholder="Verification Code" autocomplete="off"/>
            <input type="password" bind:value="{logPassword}" class="form-control login" placeholder="New Password" autocomplete="off" on:keydown="{event => event.which === 13 && resetPassword()}"/>
            <button class="btn btn-success" on:click="{resetPassword}" disabled="{logLoading}">
                {#if logLoading}
                    <i class="fa fa-spinner fa-pulse"></i>
                {:else}
                    <i class="fa fa-refresh"></i> Reset Password
                {/if}
            </button>
        </div>
    {/if}
{/if}

<div id="divider"></div>

{#if showSignUp}
    {#if signUpFlow == 0}
        <div id="signUp" class="container-fluid">
            <h6 style="text-align:center;">Sign Up For An Account</h6>
            {#if showRightMsg}
                <ErrMsg message={message} />
            {/if}
            <input class="form-control login" placeholder="name" autocomplete="off" bind:value="{regName}"/>
            <input class="form-control login" placeholder="email" autocomplete="off" bind:value="{regEmail}"/>
            <input class="form-control login" placeholder="username" autocomplete="off" bind:value="{regUsername}"/>
            <input type="password" class="form-control login" placeholder="password (min 8 characters)" autocomplete="off" bind:value="{regPassword}"/>
            <input type="password" class="form-control login" placeholder="confirm password" autocomplete="off" bind:value="{regConPassword}" on:keydown="{event => event.which === 13 && register()}"/>
            <button class="btn btn-success" on:click="{register}" disabled="{regLoading}">
                {#if regLoading}
                    <i class="fa fa-spinner fa-pulse"></i>
                {:else}
                    <i class="fa fa-user-plus"></i> Register
                {/if}
            </button>

            {#if screenWidth <= 1024}
                <p style="text-align:center;margin-top:20px;cursor:pointer;" on:click="{() => {showSignIn = true; showSignUp = false; }}">Already Have an Account? <span style="color:blue;">Sign In</span></p>
            {/if}
        </div>
    {:else if signUpFlow == 1}
        <div id="signUp" class="container-fluid" style="margin-top:20%;">
            <h6 style="text-align:center;">Check Your Email for Code</h6>
            {#if showRightMsg}
                <ErrMsg message={message} />
            {/if}
            <input class="form-control login" placeholder="code" autocomplete="off" bind:value="{regCode}" on:keydown="{event => event.which === 13 && regCode()}"/>
            <button class="btn btn-primary" style="float:left;margin-left:0px;margin-top:20px;width:30%;" on:click="{resendCode}">Resend</button>
            <button class="btn btn-success" style="float:right;width:30%;" on:click="{confirmCode}" disabled="{regLoading}">
                {#if regLoading}
                    <i class="fa fa-spinner fa-spin"></i>
                {:else}
                    Confirm
                {/if}
            </button>
        </div>
    {:else if signUpFlow == 2}
        <div id="signUp" class="container-fluid" style="margin-top:25%;">
            <h5 style="text-align:center;"><i class="fa fa-arrow-left"></i> Sign In with Your Crednetials</h5>
        </div>
    {/if}
{/if}

<style>

    #signIn {
        width:350px;
        left:20%;
        z-index:2;
        position:fixed;
        margin-top:10%;
    }

    #signUp {
        width:350px;
        right:20%;
        z-index:2;
        position:fixed;
        margin-top:12%;
    }

    .login {
        background:black;
        outline:none;
        border-radius:0.4rem;
        border:none;
        margin-top:20px;
    }

    #divider {
        z-index:4;
        width:2px;
        height:70%;
        background-color: black;
        position:fixed;
        left:50%;
        top:15%;
    }

    .btn {
        margin-top:20px;
        width:40%;
        margin-left:30%;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    #Logo {
		height:50px;
        z-index:100;
        display: block;
	}
/*
    #status {
        z-index: 999;
        position: fixed;
        top: 20px;
        right: 20px;
        width:20%;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
        background-color: var(--msg-color);
    }
*/
    @media screen and (max-width: 1024px) {
        
        #signUp {
            width:50%;
            right:25%;
            margin-top:50px;
            position:none;
        }

        #divider {
            display:none;
        }

        #signIn {
            width:50%;
            left:25%;
            margin-top:50px;
            position:none;
        }
/*
        #status {
            width:80%;
            right: 10%;
        }
*/
    }

    @media screen and (max-width: 720px) {

        #Logo {
            height: 25px;
        }
        
        #signUp {
            width:90%;
            right:5%;
            margin-top:20px;
            position:none;
        }

        #signIn {
            width:90%;
            left:5%;
            margin-top:20px;
            position:none;
        }

        .btn {
            width:60%;
            margin-left:20%;
        }

    }
</style>