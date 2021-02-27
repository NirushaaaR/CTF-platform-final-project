function makeTimer() {
    let endTime = new Date("{{game.period.end|date:'U'}}" * 1000);
    endTime = (Date.parse(endTime) / 1000);

    const now = (Date.parse(new Date()) / 1000);

    let timeLeft = endTime - now;

    let days = Math.floor(timeLeft / 86400);
    let hours = Math.floor((timeLeft - (days * 86400)) / 3600);
    let minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
    let seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

    if (hours < "10") { hours = "0" + hours; }
    if (minutes < "10") { minutes = "0" + minutes; }
    if (seconds < "10") { seconds = "0" + seconds; }

    $("#days").html(days + " Days");
    $("#hours").html(hours + " Hours");
    $("#minutes").html(minutes + " Minutes");
    $("#seconds").html(seconds + " Seconds");

}
makeTimer();
setInterval(makeTimer, 1000);
