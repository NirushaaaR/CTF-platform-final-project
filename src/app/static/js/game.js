const date_list = [];
var chartOptions = {
    chart: {
        height: 350,
        type: 'line',
    },
    xaxis: {
        type: 'numeric',
        labels: {
            show: false
        },
        tooltip: {
            enabled: false
        }
    },
    dataLabels: {
        enabled: false
    },
    series: [],
    tooltip: {
        x: {
            formatter: function (val, {
                dataPointIndex
            }) {
                const date = new Date(date_list[dataPointIndex]);
                let minute = date.getMinutes();
                minute = minute < 10 ? `0${minute}` : minute;
                return `${date.toDateString()} at ${date.getHours()}:${minute}`;
            }
        }
    }
}

var chart = new ApexCharts(
    document.querySelector("#chart-area"),
    chartOptions
);

chart.render();

function toggleAlert(message, success) {
    const alertElem = `<div class="message container">
    <div class="alert alert-${success ? "success" : "danger"} alert-dismissible text-center" role="alert">
        <button class="close" type="button" data-dismiss="alert"><span aria-hidden="true">&times;</span></button>
        <strong>${message}</strong>
    </div>
  </div>`;
  
    $(".alert-fixed-top").append(alertElem);
    setTimeout(() => {
      $(".message").fadeOut('slow');
    }, 3000);
  }

async function get_top10_score() {
    const res = await fetch(SCORE_URL);
    const json = await res.json();
    console.log("get_top10_score", json);

    const score_data = [];
    // update graph
    json.data.forEach((d, index) => {

        if (index > 0 && d.points_gained === 0) {
            return;
        }

        const idx = score_data.findIndex(s => s.name === d.username);
        if (idx >= 0) {
            // add to existing user data
            score_data[idx].current_score += d.points_gained

            for (let i = 0; i < score_data.length; i++) {
                score_data[i].data.push(score_data[i].current_score);
            }

        } else {
            // update others user data
            for (let i = 0; i < score_data.length; i++) {
                score_data[i].data.push(score_data[i].current_score);
            }
            const newUserSeries = {
                name: d.username,
                data: [...date_list.map(dl => 0), d.points_gained],
                current_score: d.points_gained,
            }
            // add new user data
            score_data.push(newUserSeries);
            chart.appendSeries(newUserSeries);
        }
        date_list.push(d.answered_at);
    });

    score_data.sort((a, b) => b.current_score - a.current_score);
    chart.updateSeries(score_data);
}

get_top10_score();

// user answer the flag
$(".form-challenge").submit(function (e) {
    e.preventDefault();
    const form = $(this);
    const url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        error: function(xhr, ajaxOptions, err) {
            toggleAlert(`Error: ${xhr.status} ${err.message}`, false);
        },
        success: function (data) {
            toggleAlert(data.message, data.correct);
            $('.input-challenge-flag').val('');
            if (data.correct) {
                // location.reload();
                get_top10_score();
                // find the right flag and update it
                const flagInfo = $("#flag_" + data.flagid);
                // status to "Solved "+ "\u2713"
                const flagStatus = flagInfo.find(".flag-status");
                flagStatus.text("Solved " + "\u2713");
                flagStatus.removeClass("text-danger");
                flagStatus.addClass("text-success");
                // point gain update
                flagInfo.find(".flag-point").text(data.points_gained);
            }
        }
    });
});