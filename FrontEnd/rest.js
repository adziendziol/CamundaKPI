

function getTasksCall(callback){
        var taskOverviewValues = [];
        var request = new XMLHttpRequest()
        // Open a new connection, using the GET request on the URL endpoint
        request.open('GET', 'http://127.0.0.1:5000/Tasks', true)

        request.onload = function() {
        // Begin accessing JSON data here
                var data = JSON.parse(this.response)
                taskOverviewValues.push(['Taskname','Anzahl'])
                if (request.status >= 200 && request.status < 400) {
                data.forEach(task => {
                taskOverviewValues.push([task.Name,task.count])
                })
                console.log(taskOverviewValues);
                callback(taskOverviewValues,'Aktuelle Anzahl der Tasks','tasksPiechart');
                } else {
                console.log('error')
                }
        }

        request.send()
};

function getHistoryTasksCall(callback){

        var historyTaskOverviewValues = [];
        var request = new XMLHttpRequest()
        // Open a new connection, using the GET request on the URL endpoint
        request.open('GET', 'http://127.0.0.1:5000/HistoryTasks', true)

        request.onload = function() {
                // Begin accessing JSON data here
                var data = JSON.parse(this.response)
                historyTaskOverviewValues.push(['Taskname','Anzahl'])
                if (request.status >= 200 && request.status < 400) {
                data.forEach(task => {
                historyTaskOverviewValues.push([task.Name,task.count])
                })
                console.log(historyTaskOverviewValues);
                callback(historyTaskOverviewValues,'Gesamte Anzahl der Abgeschlossesesn Tasks','historicTasksPiechart');
                } else {
                console.log('error')
                }
        }

        request.send()
        
}

function getKpiEventsCall(callback){

        var KpiEventValues = [];
        var request = new XMLHttpRequest()
        // Open a new connection, using the GET request on the URL endpoint
        request.open('GET', 'http://127.0.0.1:5000/KpiEvents', true)

        request.onload = function() {
                // Begin accessing JSON data here
                var data = JSON.parse(this.response)
                KpiEventValues.push(['StatusName','Anzahl'])
                if (request.status >= 200 && request.status < 400) {
                data.forEach(task => {
                KpiEventValues.push([task.StatusName,task.count])
                })
                console.log(KpiEventValues);
                callback(KpiEventValues,'Anzahl der unterschiedlichen Events','kpiEventChart');
                } else {
                console.log('error')
                }
        }

        request.send()
}


function getTimeLineInfos(callback){

        var KpiEventValues = [];
        var request = new XMLHttpRequest()
        // Open a new connection, using the GET request on the URL endpoint
        request.open('GET', 'http://127.0.0.1:5000/ProcessTimelines', true)

        request.onload = function() {
                // Begin accessing JSON data here
                var data = JSON.parse(this.response)
                //KpiEventValues.push(['Business Key','Start','Ende'])
                if (request.status >= 200 && request.status < 400) {
                data.forEach(task => {
                KpiEventValues.push([task.BusinessKey,task.ProcessName,new Date(task.StartTime),new Date(task.EndTime)])
                })
                console.log(KpiEventValues);
                callback(KpiEventValues,'Laufzeit von Fertigen Prozessen','timeLineChart');
                } else {
                console.log('error')
                }
        }

        request.send()
}

function getSingleTimeLineInfos(BusinessKeytoSend,callback){

        var KpiEventValues = [];
        var request = new XMLHttpRequest()
        console.log(BusinessKeytoSend.concat('---Function'));

        // Open a new connection, using the GET request on the URL endpoint
        var url = 'http://127.0.0.1:5000/Processtimeline/'.concat(BusinessKeytoSend)
        console.log(url)
        request.open('GET', url, true)

        request.onload = function() {
                // Begin accessing JSON data here
                var data = JSON.parse(this.response)
                //KpiEventValues.push(['Business Key','Start','Ende'])
                if (request.status >= 200 && request.status < 400) {
                data.forEach(task => {
                KpiEventValues.push([task.BusinessKey,task.ProcessName,new Date(task.StartTime),new Date(task.EndTime)])
                })
                console.log(KpiEventValues);
                callback(KpiEventValues,'Laufzeit von Fertigen Prozessen','timeLineChart');
                } else {
                console.log('error')
                }
        }

        request.send()
}

