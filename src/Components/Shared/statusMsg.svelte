<script>
    export let heading, message, status;

    document.documentElement.style.setProperty('--msg-color', status);
</script>

<div id="errtemp">
    <h5 id="heading">{heading}</h5>
    <p id="body">{message}</p>
</div>

<style>
    #errtemp {
        background-color: var(--msg-color);
        height:100%;
        margin-bottom:20px;
    }

    #heading {
        color:white;
        margin-top:20px;
    }

    #body {
        margin-top:15px;
        color:white;
    }
</style>