function origin() {
    let ws = new WebSocket("ws://" + window.location.host + ':81');

    ws.onopen = function () {

    };

    ws.onmessage = function (evt) {
        $('#origin_img')[0].src = 'data:image/png;base64,' + evt.data;
    };

    ws.onclose = function () {

    };
}

let array = new Array(24);
for (let i = 0; i < 24; i++) {
    array[i] = i + 1
}

var config = {
    type: 'line',
    data: {
        xLabels: array,
        yLabels: ['极高', '高', '中等', '低'],
        datasets: [{
            label: '密度级别',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [],
            fill: false
        }]
    },
    options: {
        responsive: true,
        title: {
            display: false,
            text: '密度记录表'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            enabled: false
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '帧数'
                }
            }],
            yAxes: [{
                type: 'category',
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '密度级别'
                }
            }]
        }
    }
};

var index = 0;

function result() {
    let ws = new WebSocket("ws://" + window.location.host + ':82');
    ws.onopen = function () {

    };

    ws.onmessage = function (evt) {
        let data = $.parseJSON(evt.data);
        let level = '低';
        switch (data.result) {
            case 0:
                level = '低';
                break;
            case 1:
                level = '中等';
                break;
            case 2:
                level = '高';
                break;
            case 3:
                level = '极高';
                break;
        }
        $('#process_img')[0].src = 'data:image/png;base64,' + data.img;
        $('#crowd_result').text(level);


        config.data.datasets.forEach(function (dataset) {
            if (config.data.datasets[0].data.length >= 24) {
                dataset.data.splice(0, 1);
            }
            dataset.data.push(level);
        });
        window.myLine.update();
    };
}

function update_time() {
    let time = new Date();
    let day = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    let local_time = time.toLocaleTimeString();
    let local_day = day[time.getDay()];
    $('#time').text(local_day + " " + local_time);
}


self.setInterval("update_time()", 1000);

window.onload = function () {
    let ctx = document.getElementById('chart').getContext('2d');
    window.myLine = new Chart(ctx, config);
    result();
    origin();
};
