google.charts.load('current', {'packages':['line', 'corechart']});
google.charts.setOnLoadCallback(gfs);

var state = [ 0 ];


function getData () {
    $.get("https://wodeyuce.herokuapp.com/data.json", function (jsonresponse) {
        localStorage["data"] = JSON.stringify(jsonresponse);
    }, "json");

    var data = new google.visualization.DataTable(localStorage["data"]);
    return data;
}


function satellite () {
    var chart = document.getElementById('lineplot');
    var satimg = document.getElementById('satellite');

    chart.style.display = "none";
    if (satimg.style.display == "none") {
        satimg.style.display = "block";
    }

}

function nwp () {
    var chart = document.getElementById('lineplot');
    var satimg = document.getElementById('satellite');

    satimg.style.display = "none";
    if (chart.style.display == "none") {
        chart.style.display = "block";
    }
    state = [0, 1, 2, 3, 4];
    var data = new google.visualization.DataTable(
        localStorage["data"]);
    var view = new google.visualization.DataView(data);
    view.setColumns(state);
    drawLineChart(view);
}

function gfs () {
    var data = getData();
    drawLineChart(data);
}

function stateColumns(val) {
    if (state.includes(val)) {
        const index = state.indexOf(val);
        if (index > -1) {
            state.splice(index, val);
        }
    } else {
        state.push( val )
    }
}

function changeState(val) {
    var data = new google.visualization.DataTable(
        localStorage["data"]);

    var view = new google.visualization.DataView(data);
    stateColumns(val);
    view.setColumns(state);
    drawLineChart(view);
}

function drawLineChart(data) {
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
