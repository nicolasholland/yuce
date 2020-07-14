google.charts.load('current', {'packages':['line', 'corechart']});
google.charts.setOnLoadCallback(drawLineChart);


function getData () {
    $.get("http://wodeyuce.herokuapp.com/data.json", function (jsonresponse) {
        localStorage["data"] = JSON.stringify(jsonresponse);
    }, "json");

    var data = new google.visualization.DataTable(localStorage["data"]);
    return data;
}

function state1() {
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
