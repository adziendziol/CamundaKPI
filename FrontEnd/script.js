var historyTaskOverviewValuesTest = [];
google.charts.load('current', {'packages':['corechart','timeline','table']});

$(document).ready(function(){
    google.charts.setOnLoadCallback(startup)    
});

function startup(){
       getKpiOverview(drawTableChart);
       getHistoryTasksCall(drawChart);
       getTasksCall(drawChart);
       getKpiEventsCall(drawChart);
       getTimeLineInfos(drawTimeLine);
};

 
function sleep(milliseconds) {
        var start = new Date().getTime();
        for (var i = 0; i < 1e7; i++) {
                if ((new Date().getTime() - start) > milliseconds){
                break;
                }
        }
}


function drawChart(values,title,elementID) {
        var data = google.visualization.arrayToDataTable(values);
        var options = {
          title: title
        };
        var chart = new google.visualization.PieChart(document.getElementById(elementID));

        chart.draw(data, options);
}

function drawPointChart(values,title,elementID) {
        var data = google.visualization.arrayToDataTable(values);

        var options = {
          title: title,
          hAxis: {title: 'Age', minValue: 0, maxValue: 15},
          vAxis: {title: 'Weight', minValue: 0, maxValue: 15},
          legend: 'none'
        };

        var chart = new google.visualization.ScatterChart(document.getElementById(elementID));

        chart.draw(data, options);
      }


function drawTimeLine(values,title,elementID) {
        var data = new google.visualization.DataTable();
        
        data.addColumn({ type: 'string', id: 'Order' });
        data.addColumn({ type: 'string', id: 'SubProcess' });
        data.addColumn({ type: 'date', id: 'Start' });
        data.addColumn({ type: 'date', id: 'End' });
        data.addRows(values);

        var options = {
          title: title,
          timeline: { showRowLabels: true }
        };
        var chart = new google.visualization.Timeline(document.getElementById(elementID));
        chart.draw(data, options);
      }
      
function updateTimeLineWithOneBusinessKey(){
        var BusinessKey = document.getElementById('businessKeyInput').value
        console.log(BusinessKey)
        getSingleTimeLineInfos(BusinessKey,drawTimeLine)
}

function UpdateKpiReport(){
        UpdateKpiReportCall()
}

function drawTableChart(values,title,elementID) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Name');
        data.addColumn('number', 'KPI-Wert (in Tagen)');
        data.addColumn('boolean', 'KPI-Gehalten?');
        data.addColumn('number', 'Anzahl');
        data.addRows(values);
        var options = {
          title: title
        };
        var chart = new google.visualization.Table(document.getElementById(elementID));

        chart.draw(data, options);
}