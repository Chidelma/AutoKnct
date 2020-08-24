<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js';

    export let xValues, yValues, rightYValues;

    function createSearchChart() {
        let ctx = document.getElementById('sChart').getContext('2d');

        let dataSet = [{ label : "Average Bid", yAxisID : "Prices", data : yValues, borderWidth : 1, backgroundColor : 'rgba(255, 99, 132, 0.2)', borderColor : 'rgba(255,99,132,1)' }, { label : "Vehicle Count", yAxisID : "Count", data : rightYValues, borderWidth : 1, backgroundColor : 'rgba(132, 99, 255, 0.2)', borderColor : 'rgba(132,99,255,1)' }];
        
        let yAxis = [{ id: 'Prices', type: 'linear', position: 'left', gridLines: { display: false } }, { id: 'Count', type: 'linear', position: 'right', gridLines: { display: false } }];

        let data = {
            labels: xValues,
            datasets: dataSet
        };

        let options = {
            maintainAspectRatio: false,
            scales: {
                yAxes: yAxis,
                xAxes: [{
                    ticks: {
                        min: 0,
                        beginAtZero: true
                    },
                    gridLines: {
                        display: false
                    }
                }]
            }
        };

        var sChart = new Chart(ctx, {
            options: options,
            data: data,
            type: 'line'
        });
    }

    onMount(createSearchChart);
</script>

<canvas id="sChart" width="400" height="400"></canvas>
