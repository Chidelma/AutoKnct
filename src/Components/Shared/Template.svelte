<script>
    import { invokeLambda } from './../../Scripts/Lambda.js';
    import { currUser, tabIndex, garageIndex } from './../../Scripts/Init.js';
    import { queryResults, convertToCurrency } from './../../Scripts/Filter.js';
    import { Analytix } from './../../Scripts/Analytics.js';
    //import { ChartPlot } from './../../Scripts/Chart.js';
    import { fly } from 'svelte/transition';
    import Message from './statusMsg.svelte';
    import Modal from './Modal.svelte';
    import Chart from './Chart.svelte';
    import env from './../../env.json';
    import { beforeUpdate, afterUpdate } from 'svelte';

    let div, autoscroll;

    export let id, year, model, url, vin, cyl, status, price, mileage, date, images; 

    let Payload;

    let showMsg = false, heading = '', message = '', statusColor = ''; 

    let ratio = screen.width / screen.height;

    let addComapare = $currUser.compare.length == 7 ? true : false;

    setInterval(function() {
        addComapare = $currUser.compare.length == 7 ? true : false;
    }, 1000);

    document.documentElement.style.setProperty('--msg-color', statusColor);

    let viewAnalytics = false, analytics = null, currModel, currYear, nullPrice = false, xValues = [], yValues = [], analyticErr = false;
    
    let userComment;

    let i = 0;

    let viewImages = false, currImage = images != undefined ? images[i] : [];

    let screenWidth = screen.width;

    let leftMarginMob = (screen.width - 500) / 2;

    let marginLeftMob = (screen.width - 350) / 2;

    let garResults = [];

    document.documentElement.style.setProperty('--left-margin-mob', leftMarginMob + 'px');

    document.documentElement.style.setProperty('--margin-left-mob', marginLeftMob + 'px');

    if(ratio > 1.6) {
        document.documentElement.style.setProperty('--left-margin', '4.5%');
    }
    if(ratio < 1.6) {
        document.documentElement.style.setProperty('--left-margin', '8.5%');
    }
    if(ratio == 1.6) {
        document.documentElement.style.setProperty('--left-margin', '6.5%');
    }

    function checkExist(id, garType) {

        if(garType == 'owned'){

            if($currUser.owned.length > 0) {

                for(let i = 0; i < $currUser.owned.length; i++) {

                    if($currUser.owned[i]._id == id)
                        return true

                }

                return false;

            }
            else 
                return false;
            
        }

        if(garType == 'comapare'){

            if($currUser.compare.length > 0) {

                for(let i = 0; i < $currUser.compare.length; i++) {

                    if($currUser.compare[i]._id == id)
                        return true;

                }

                return false;

            }
            else 
                return false;
            
        }

        if(garType == 'shared') {

            if($currUser.shared.length > 0) {

                for(let i = 0; i < $currUser.shared.length; i++) {

                    if($currUser.shared[i]._id == id)
                        return true;

                }

                return false;

            }
            else 
                return false;
        }
    }

    function addToGarage(id, garType) {

        if(!checkExist(id, garType)) {

            Payload = { 
                func : 'addToGarage',
                map : garType, 
                autoID : id
            }

            invokeLambda(env.lambda.pythonAPI, Payload).then(async (response) => {

                console.log(response);

                showMsg = true, heading = 'Success!', message = 'Vehicle Added To Garage', statusColor = 'green'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

                await $currUser.update(state => {
                    state.updateGarage(response);
                    return state;
                });

            }).catch((err) => {

                showMsg = true, heading = 'Error - Garage', message = err, statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            });

        }
        else {

            showMsg = true, heading = 'Error - Garage', message = "This Vehicle Already Exist In Your Garage", statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        }
    }

    function removeAuto(id, garType) {

        Payload = { 
            func : 'removeAuto',
            map : garType, 
            autoID : id
        }

        invokeLambda(env.lambda.pythonAPI, Payload).then(async (response) => {

            console.log(response);

            showMsg = true, heading = 'Success!', message = 'Vehicle Removed From Garage', statusColor = 'green'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

            await $currUser.update(state => {
                state.updateGarage(response);
                return state;
            });

        }).catch((err) => {

            showMsg = true, heading = 'Error - Garage', message = err, statusColor = 'red'; 

            setTimeout(function(){ 
                showMsg = false, heading = '', message = '', statusColor = ''; 
            }, 2000);

        });
    }

    function Analytics(vin, model, year) {

        viewAnalytics = true;

        currModel = model, currYear = year

        Payload = { 
            func : 'getAnalytics',
            vin : vin, 
            model : model,
            year : year,
        };

        invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

            if(response.count != undefined) {

                analytics = new Analytix(response);

                for(let i = 0; i < analytics.autoHist.length; i++)
                    if(analytics.autoHist[i].Price == null)
                        nullPrice = true;

                for(let i = 0; i < analytics.chartList.length; i++) {
                    xValues.push(analytics.chartList[i].Date); 
                    yValues.push(analytics.chartList[i].Price);
                }

                autoscroll = div && (div.offsetHeight + div.scrollTop) > (div.scrollHeight - 20);
            }
            else {
                console.log(response);
                analyticErr = true;
            }

        }).catch((err) => {

            console.log(err);

            analyticErr = true;

        });
    }

    document.documentElement.style.setProperty('--view-comments', 'none');
    document.documentElement.style.setProperty('--view-analytic', 'block');

    function toggleComments() {
        document.documentElement.style.setProperty('--view-comments', 'block');
        document.documentElement.style.setProperty('--view-analytic', 'none');
    }

    function toggleAnalytics() {
        document.documentElement.style.setProperty('--view-comments', 'none');
        document.documentElement.style.setProperty('--view-analytic', 'block');
    }


    function postComment(id, year, model) {

        if(userComment != '') {

            Payload = { 
                func : 'postComment',
                vin : vin, 
                name : $currUser.Name,
                autoID : id != null ? id : null,
                userID : $currUser.user_id,
                date : moment().format("YYYYMMDD, HH:mm"),
                text : id != null ? year + ' ' + model : userComment 
            };

            if (autoscroll) div.scrollTo(0, div.scrollHeight);

            invokeLambda(env.lambda.pythonAPI, Payload).then((response) => {

                console.log(response);

                analytics.setComments(response);

                userComment = '';

            }).catch((err) => {

                showMsg = true, heading = 'Error - Comments', message = err, statusColor = 'red'; 

                setTimeout(function(){ 
                    showMsg = false, heading = '', message = '', statusColor = ''; 
                }, 2000);

            });
        }
    }

    function nextImage() {
        i += 1;
        if(images[i] == undefined || images[i] == null) {
            i = 0; currImage = images[i]; 
        }
        else {
            currImage = images[i]; 
        }
    }

    function prevImage() {
        i -= 1;
        if(images[i] == undefined || images[i] == null) {
            i = images.length - 1; currImage = images[i]; 
        }
        else {
            currImage = images[i]; 
        }
    }

    function getTimeSpan(date) {
        return moment(date, "YYYYMMDD, HH:mm").fromNow();
    }
</script>

{#if showMsg}
    <div id="status" class="container-fluid" in:fly="{{ x:200, duration:500 }}" out:fly="{{ x:200, duration:500 }}">
        <Message heading={heading} message={message} status={statusColor} />
    </div>
{/if}

{#if $tabIndex == 2 && $garageIndex == 1}
    <table style="float:left;font-size:13px" width="155" height="300" border="0" cellpadding="3">
        <tr>
            <td align="center">
                <div>
                    {#if url == "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"}
                        <img style="width:75%;height:75%;margin-left:12.5%;" src="{url}" alt="Image"/>
                    {:else}
                        <img class="image" src="{url}" alt="Image" on:click="{() => viewImages = true}"/>
                    {/if}
                </div>
            </td>
        </tr>
        <tr style="border-bottom:1px solid black;">
            <td align="center">
                <div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:155px">
                    <span class="makeVal">{model}</span>
                </div>
            </td>
        </tr>
        <tr style="border-bottom:1px solid black;">
            <td align="center">
                {#if year != null}
                    <span class="yearVal">{year}</span>
                {/if}
            </td>
        </tr>
        <tr>
            <td align="center" style="border-bottom:1px solid black;">
                <span class="vinVal">{vin}</span>
            </td>
        </tr>
        <tr>
            <td align="center" style="border-bottom:1px solid black;">
                <span class="cylVal">{cyl}</span>
            </td>
        </tr>
        <tr>
            <td align="center" style="border-bottom:1px solid black;">
                <span class="statusVal">{status}</span>
            </td>
        </tr>
        <tr>
            <td align="center" style="border-bottom:1px solid black;">
                <span class="mileVal">{mileage}</span>
            </td>
        </tr>
        <tr>
            <td align="center" style="border-bottom:1px solid black;">
                <span class="dateVal">{date}</span>
            </td>
        </tr>
        <tr>
            <td align="center" style="border-bottom:1px solid black;">
                {#if price != null}
                    <span class="bidVal" style="color:green;">${convertToCurrency(price)}</span>
                {:else}
                    <span class="labelVal"><b>Pending</b></span>
                {/if}
            </td>
        </tr>
        <tr>
            <td>
                <button class="btn btn-sm btn-light compbtn" style="outline:none;width:100%;" on:click="{() => Analytics(vin, model, year)}"><i class="fa fa-area-chart"></i> View Analytics</button>
            </td>
        </tr>
        <tr>
            <td>
                <button class="btn btn-sm btn-light compbtn" style="outline:none;width:100%;" on:click="{() => addToGarage(id, 'owned')}" disabled="{checkExist(id, 'owned')}"><i class="fa fa-plus"></i> Add To Garage</button>
            </td>
        </tr>
        <tr>
            <td>
                <button class="btn btn-sm btn-danger compbtn" style="outline:none;width:100%;" on:click="{() => removeAuto(id, 'compared')}"><i class="fa fa-remove"></i> Remove</button>
            </td>
        </tr>
    </table>
{:else}
    <table class="tableResults" cellpadding="2"> 
        <tr>
            <td colspan="3" class="title">
                <div class="title-inner"> 
                    <span>
                        <b> 
                        {#if year != null}
                            {year} 
                        {/if}
                            {model}
                        </b>
                    </span>
                </div>
            </td>
        </tr>
        <tr>
            <td style="width:40%">
                <div>
                    {#if url == "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"}
                        <img style="width:75%;height:75%;margin-left:12.5%;" src="{url}" alt="Image"/>
                    {:else}
                        <img class="image" src="{url}" alt="Image" on:click="{() => viewImages = true}"/>
                    {/if}
                </div>
            </td> 
            <td>
                <span class="label">VIN</span>
                <span class="labelVal">
                    <b>
                        {#if vin == null || vin == ''}
                            Unavailable
                        {:else}
                            {vin}
                        {/if}
                    </b>
                </span>

                <span class="label">CYL</span>
                {#if cyl == null || cyl == '' || cyl == 'null'}
                    <span class="labelVal"><b>Unavailable</b></span>
                {:else}
                    <span class="labelVal"><b>{cyl}</b></span>
                {/if}

                <span class="label">Status</span>
                <span class="labelVal"><b>{status}</b></span>
            </td>
            <td>
                <span class="label">Final Bid</span>
                {#if price != null}
                    <span class="labelVal" style="color:green"><b>${convertToCurrency(price)}</b></span>
                {:else}
                    <span class="labelVal"><b>Pending</b></span>
                {/if}

                <span class="label">Mileage</span>
                {#if mileage != null}
                    <span class="labelVal"><b>{mileage} km</b></span>
                {:else}
                    <span class="labelVal"><b>Unavailable</b></span>
                {/if}

                <span class="label">Date</span>
                <span class="labelVal"><b>{date}</b></span>
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <button id="compare" class="btn btn-light btn-sm" style="width:33.3%;float:left;" disabled="{addComapare}" on:click="{() => addToGarage(id, 'compared')}"><i class="fa fa-balance-scale"></i> Compare</button>
                <button id="compare" class="btn btn-light btn-sm" style="width:33.3%;" on:click="{() => Analytics(vin, model, year)}"><i class="fa fa-area-chart"></i> View Analytics</button>
                {#if $tabIndex != 2}
                    <button id="garage" class="btn btn-light btn-sm" style="width:33.3%;float:right" on:click="{() => addToGarage(id, 'owned')}"><i class="fa fa-plus"></i> Add To Garage</button>
                {:else}
                    {#if $garageIndex == 0}
                        <button id="garage" class="btn btn-danger btn-sm" style="width:33.3%;float:right" on:click="{() => removeAuto(id, 'owned')}"><i class="fa fa-trash"></i> Remove</button>
                    {:else if $garageIndex == 2}
                        <button id="garage" class="btn btn-danger btn-sm" style="width:33.3%;float:right" on:click="{() => removeAuto(id, 'shared')}"><i class="fa fa-trash"></i> Remove</button>
                    {/if}
                {/if}
            </td>
        </tr>
    </table>
{/if}

{#if viewImages}
    <Modal/>
    <div id="autoImages" class="container-fluid">
        <button id="closeAnalytics" class="btn btn-danger" style="border-radius:50%;float:right;margin-top:20px;" on:click="{() => viewImages = false}"><i class="fa fa-times"></i></button>
        
        <img id="first-image" class="col-md-12" alt="First Image" src="{currImage}" />
        
        {#if screenWidth > 1024}
            <div style="width:100%;margin-top:20px;">
                {#each images as image}
                    <img class="all-images" alt="Current Image" src="{image}" style="bottom:10px;background-color:transparent;cursor:pointer;margin-top:30px;" on:click="{() => currImage = image}"/>
                {/each}
            </div>
        {:else}
            <div style="margin-top:100px;width:100%;">
                <button class="btn btn-primary btn-lg" style="float:left" on:click="{prevImage}">Prev</button>
                <button class="btn btn-primary btn-lg" style="float:right" on:click="{nextImage}">Next</button>
                <h3 style="text-align:center;color:white;">{i + 1}/{images.length}</h3>
            </div>
        {/if}
    </div>
{/if}

{#if viewAnalytics}
    <Modal/>
    {#if screenWidth > 1024}
        <button id="closeAnalytics" class="btn btn-danger" style="border-radius:50%;right:20px;top:5px;z-index:50;position:fixed;" on:click="{() => viewAnalytics = false}"><i class="fa fa-times"></i></button>
    {/if}
    <div id="autoAnalytics" class="container-fluid">

        {#if screenWidth <= 1024}
            <button id="closeAnalytics" class="btn btn-danger btn-sm" style="float:left;margin-top:10px;font-size:20px;" on:click="{() => viewAnalytics = false}">Close</button>
            <button id="closeAnalytics" class="btn btn-dark btn-sm" style="float:right;margin-top:10px;font-size:20px;" on:click="{toggleComments}">View Comments <i class="fa fa-arrow-right"></i></button>
        {/if}

        <h3 class="analyticHeader">{currYear} {currModel} Analytics</h3>
        
        {#if analyticErr == false && analytics == null}
            <div class="text-center">
                <img src="https://autoarch.blob.core.windows.net/resources/loader.gif" alt="Loader"/>
            </div>
            <h6 style="text-align:center;">Loading...</h6>
        {:else if analyticErr == true && analytics == null}
            <h5 style="text-align:center;margin-top:20%;">Analytics Unavailable For This Vehicle</h5>
        {:else}
            <div class="box-body" style="margin-top:20px;padding:0px 15px 0px 15px">
                <div id="lytiChart" class="chart-container">
                    <Chart xValues={xValues} yValues={yValues} />
                </div>
            </div>

            <h4 style="margin-top:10px;width:100%;text-align:center;">Vehicle Detail History</h4>

            {#each analytics.autoHist as auto} 
                <table class="analyticAutos" cellpadding="2" align="center"> 
                    <tr>
                        <td colspan="3" class="title">
                            <div class="title-inner"> 
                                <span>
                                    <b> 
                                    {#if auto.Year != null}
                                        {auto.Year} 
                                    {/if}
                                        {auto.Model}
                                    </b>
                                </span>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td style="width:40%">
                            <div>
                                {#if url == "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"}
                                    <img style="width:75%;height:75%;margin-left:12.5%;" src="{url}" alt="Image"/>
                                {:else}
                                    <img class="image" src="{auto.Images[0]}" alt="Image"/>
                                {/if}
                            </div>
                        </td> 
                        <td >
                            <span class="label">VIN</span>
                            <span class="labelVal"><b>{auto.VIN}</b></span>

                            <span class="label">CYL</span>
                            <span class="labelVal"><b>{auto.CYL}</b></span>

                            <span class="label">Status</span>
                            <span class="labelVal"><b>{auto.Status}</b></span>
                        </td>
                        <td>
                            {#if price != null}
                                <span class="label">Final Bid</span>
                                <span class="labelVal" style="color:green"><b>${convertToCurrency(auto.Price)}</b></span>
                            {:else}
                                <span class="label">Final Bid</span>
                                <span class="labelVal"><b>Pending</b></span>
                            {/if}

                            <span class="label">Mileage</span>
                            <span class="labelVal"><b>{auto.Mileage} km</b></span>

                            <span class="label">Date</span>
                            <span class="labelVal"><b>{auto.Date}</b></span>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="3">
                            <button id="compare" class="btn btn-light btn-sm" style="width:49.5%;float:left;" disabled="{addComapare}" on:click="{() => addToGarage(auto._id, 'compared')}"><i class="fa fa-balance-scale"></i> Compare</button>
                            <button id="garage" class="btn btn-light btn-sm" style="width:49.5%;float:right" on:click="{() => addToGarage(auto._id, 'owned')}"><i class="fa fa-plus"></i> Add To Garage</button>
                        </td>
                    </tr>
                </table>
            {/each}

            <table id="statsTable" align="center" cellpadding="2">
                <tr>
                    <td id="statsTitle" align="center" colspan="2" style="border-bottom:1px solid red">
                        <h4 style="text-align:center;width:100%">Vehicle Statistics</h4>
                    </td>
                </tr>
                <tr>
                    <td style="width:50%">
                        <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal">Auctions</h6>
                        {#if nullPrice}
                            <h6 class="details" style="float:right;width:50%;text-align:center">{analytics.numAucts - 1}</h6>
                        {:else}
                            <h6 class="details" style="float:right;width:50%;text-align:center">{analytics.numAucts}</h6>
                        {/if}
                        <br /><br />

                        <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal">Min. Final Bid</h6>
                        {#if analytics.minBid == 'Unavailable'}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">{analytics.minBid}</h6>
                        {:else}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">${convertToCurrency(analytics.minBid)}</h6>
                        {/if}

                        <br /><br />

                        <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal">Max. Final Bid</h6>
                        {#if analytics.maxBid == 'Unavailable'}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">{analytics.maxBid}</h6>
                        {:else}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">${convertToCurrency(analytics.maxBid)}</h6>
                        {/if}
                    </td>

                    <td style="border-left:1px solid red" class="details">
                        <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal">Avg. Final Bid</h6>
                        {#if analytics.avgBidPrice == 'Unavailable'}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">{analytics.avgBidPrice}</h6>
                        {:else}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">${convertToCurrency(analytics.avgBidPrice)}</h6>
                        {/if}

                        <br /><br />

                        {#if nullPrice}
                            <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal">Est. Final Bid</h6>
                            {#if analytics.avgSalePrice == 'Unavailable'}
                                <h6 class="details" style="float:right;width:50%;text-align:center;">{analytics.avgSalePrice}</h6>
                            {:else}
                                <h6 class="details" style="float:right;width:50%;text-align:center;">${convertToCurrency(analytics.avgSalePrice)}</h6>
                            {/if}
                        {:else}
                            <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal;">Avg. Related Final Bids</h6>
                            {#if analytics.avgSalePrice == 'Unavailable'}
                                <h6 class="details" style="float:right;width:50%;text-align:center;">{analytics.avgSalePrice}</h6>
                            {:else}
                                <h6 class="details" style="float:right;width:50%;text-align:center;">${convertToCurrency(analytics.avgSalePrice)}</h6>
                            {/if}
                        {/if}

                        <br /><br />

                        <h6 class="details" style="float:left;width:50%;text-align:center;font-weight:normal">Value Profit</h6>
                        {#if analytics.extData == 'Unavailable'}
                            <h6 class="details" style="float:right;width:50%;text-align:center;">{analytics.extData}</h6>
                        {:else}
                            <h6 class="details" style="float:right;width:50%;text-align:center;color:green;">${convertToCurrency(analytics.extData)}</h6>
                        {/if}
                    </td>
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
    </div>

    <div id="autoComments" class="container-fluid">
        {#if screenWidth <= 1024}
            <button id="closeAnalytics" class="btn btn-danger btn-sm" style="float:right;margin-top:10px;font-size:20px;" on:click="{() => viewAnalytics = false}">Close</button>
            <button id="closeAnalytics" class="btn btn-dark btn-sm" style="float:left;margin-top:10px;font-size:20px;" on:click="{toggleAnalytics}"><i class="fa fa-arrow-left"></i> View Analytics</button>
        {/if}
        <h3 class="analyticHeader">Comments</h3>
        {#if analyticErr == false && analytics == null}
            <div class="text-center">
                <img src="https://autoarch.blob.core.windows.net/resources/loader.gif" alt="Loader"/>
            </div>
            <h6 style="text-align:center;">Loading...</h6>
        {:else if analytics.comments == null}
            <h5 style="text-align:center;margin-top:50%;">No Comments For This Vehicle</h5>
        {:else}
            <div class="scrollable" bind:this="{div}">
                {#each analytics.comments as comment}
                    {#if comment.userID == $currUser.user_id}
                        <article class="curUser">
                            <span class="textCom">{comment.text}</span>
                            <p style="font-size:10px;">Me {getTimeSpan(comment.date)}</p>
                        </article>
                    {:else}
                        <article class="odaUser">
                            {#if comment.autoID == null}
                                <span class="textCom">{comment.text}</span>
                            {:else}
                                <span class="textShare" style="cursor:pointer;" on:click="{() => addToGarage(comment.autoID, 'shared')}">{comment.text}</span>
                            {/if}
                            <p style="font-size:10px;">{comment.name} {getTimeSpan(comment.date)}</p>
                        </article>
                    {/if}
                {/each}
                {#if garResults.length > 0 && userComment.length > 0}
                    <h6 style="text-align:center;">Garage Results</h6>
                    {#each garResults as auto}
                        <div style="padding:5px;margin-top:5px;">
                            <p style="float:left;">{auto.Year} {auto.Model}</p>
                            <button class="btn btn-info btn-sm" style="float:right;" on:click="{() => postComment(auto._id, auto.Year, auto.Model)}"><i class="fa fa-share-alt"></i> Share</button>
                        </div>
                    {/each}
                {/if}
            </div>
        {/if}
        <input id="userComet" autocomplete="off" placeholder="Type Comment Or Share Garage Vehicle" bind:value="{userComment}" on:keyup="{() => garResults = queryResults(userComment, $currUser.owned, [])}" on:keydown="{event => event.which === 13 && postComment(null, null, null)}"/>
    </div>
{/if}

<style>

    .scrollable {
		flex: 1 1 auto;
		margin: 0 0 0.5em 0;
		overflow-y: auto;
	}

	article {
		margin: 0.5em 0;
	}

	.curUser {
		text-align: right;
	}

	.textCom {
		padding: 0.5em 1em;
		display: inline-block;
	}

    .textShare {
        padding: 0.5em 1em;
		display: inline-block;
    }

	.odaUser .textCom {
		background-color: #eee;
		border-radius: 1em 1em 1em 0;
	}

    .odaUser .textShare {
        background-color: #ffc107;
		border-radius: 1em 1em 1em 0;
    }

	.curUser .textCom {
		background-color: #0074D9;
		color: white;
		border-radius: 1em 1em 0 1em;
	}

    #userComet {
        bottom:10px;
        left:10px;
        width:95%;
        border-radius:0.4rem;
        box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        outline:none;
        border:none;
        position: absolute;
    }

    .labelVal {
        display:block;
    }

    .fa {
        outline:none;
    }

    .label {
        color:#7c7c7c
    }

    .image {
        width:100%;
        height:100%;
        cursor: pointer;
    }

    .compbtn {
        box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .tableResults {
        border-radius: 0.4rem;
        background-color: white;
        box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-bottom:25px;
        height: 100px;
        width:500px;
        float : left;
        margin-left:var(--left-margin);
    }

    .analyticAutos {
        border-radius: 0.4rem;
        background-color: white;
        box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        margin-bottom:25px;
        height: 100px;
        width:500px;
    }

    .title {
        text-align: left;
        font-size:15px;
    }

    #status {
        z-index: 9999;
        position: fixed;
        top: 20px;
        right: 20px;
        width:20%;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius:0.4rem;
        background-color: var(--msg-color);
    }

    ::-webkit-scrollbar {
        width: 1px;
    }

    #autoAnalytics {
        width: 65%;
        z-index:25;
        position:fixed;
        top:20px;
        left:20px;
        bottom:20px;
        background-color:#fff;
        overflow-y:auto;
        border-radius:0.4rem;
    }

    #autoComments {
        width: 30%;
        z-index:25;
        position:fixed;
        top:20px;
        right:20px;
        bottom:20px;
        background-color:#fff;
        overflow-y:auto;
        border-radius:0.4rem;
    }

    #autoImages {
        z-index:50;
        position:fixed;
        width:100%;
        top:0;
        left:0;
        bottom:0;
        right:0;
    }

    #statsTable {
        margin-top:30px;
        margin-bottom:30px;
        width:500px;
        height: 100px;
        background-color:rgba(255, 99, 132,0.3);
        border-radius:0.4rem;
        box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    #closeAnalytics {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .text-center {
        margin-top:20%;
    }

    .all-images {
        height:200px;
        width:20%;
    }

    #first-image {
        width:50%;
        height:65%;
        margin-left:25%;
        top:25px;
    }

    .analyticHeader {
        text-align:center;
        margin-top:20px;
        margin-bottom:20px;
    }

    @media screen and (max-width: 1024px) {
        
        .tableResults {
            margin-left:var(--left-margin-mob);
            margin-bottom:25px;
        }

        #autoComments {
            display:var(--view-comments);
            left:20px;
            width:95%;
        }

        #first-image {
            width:80%;
            height:50%;
            top:70px;
            margin-left:10%;
        }

        .analyticAutos {
            margin-bottom:25px;
            margin-left:15%;
            float:unset;
        }

        #statsTable {
            margin-left:15%;
            float:unset;
        }

        #status {
            width:80%;
            right: 10%;
        }

        #autoAnalytics {
            width: 95%;
            right:20px;
            display:var(--view-analytic);
        }

        .analyticHeader {
            margin-top:60px;
        }

    }

    @media screen and (max-width: 720px) {

        .title {
            font-size:11px;
        }

        .tableResults {
            width:100%;
            margin-left:0px;
            font-size:11px;
        }

        .btn {
            font-size:11px;
        }

        #first-image {
            width:100%;
            height:35%;
            top:50px;
            margin-left:0px;
        }

        #autoAnalytics {
            width: 100%;
            top:0;
            left:0px;
            bottom:0px;
            right:0px;
        }

        #autoComments {
            width: 100%;
            top:0;
            left:0px;
            bottom:0px;
            right:0px;
        }

        .analyticAutos {
            width:100%;
            margin-left:0px;
            font-size:11px;
        }

        #statsTable {
            float:unset;
            margin-top:30px;
            margin-right:unset;
            margin-left:unset;
            width:100%;
        }

        .details {
            font-size:15px;
        }

    }
</style>