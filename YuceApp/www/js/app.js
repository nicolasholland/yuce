google.charts.load('current', {'packages':['line', 'corechart']});
google.charts.setOnLoadCallback(drawLineChart);


function getData () {
    $.get("https://wodeyuce.herokuapp.com/data.json", function (jsonresponse) {
        localStorage["data"] = JSON.stringify(jsonresponse);
    }, "json");

    var data = new google.visualization.DataTable(localStorage["data"]);
    return data;
}


function satellite () {
    var chart = document.getElementById('lineplot');
    if (chart.style.display == "block") {
        chart.style.display = "none";
    }
}

function nwp () {
    var chart = document.getElementById('lineplot');
    if (chart.style.display == "none") {
        chart.style.display = "block";
    }
}

function changeState(val) {
    getData();
    drawLineChart();
}

function drawLineChart() {
    var data = getData();

    var options = {
        title: '太阳光预测',
        curveType: 'function',
        legend: { position: 'bottom' },
        series: {
            0: {targetAxisIndex: 0}
        },
        vAxes: {
            0: {title: 'Ghi (W/m²)'}
        },
        vAxis: {
            viewWindow: {
                min: 0,
                max: 1000
            }
        }
    };

    var chart = new google.visualization.LineChart(
        document.getElementById('lineplot'));
        chart.draw(data, options);
}
