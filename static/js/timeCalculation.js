function calculateRunningTime() {
    var startDate = new Date("2018-01-01T00:00:00"); // 设置起始日期
    var now = new Date();

    // 计算时间差
    var delta = now - startDate;

    // 计算年月日时分秒
    var years = Math.floor(delta / (1000 * 60 * 60 * 24 * 365));
    delta -= years * 1000 * 60 * 60 * 24 * 365;
    var months = Math.floor(delta / (1000 * 60 * 60 * 24 * 30));
    delta -= months * 1000 * 60 * 60 * 24 * 30;
    var days = Math.floor(delta / (1000 * 60 * 60 * 24));
    delta -= days * 1000 * 60 * 60 * 24;
    var hours = Math.floor(delta / (1000 * 60 * 60));
    delta -= hours * 1000 * 60 * 60;
    var minutes = Math.floor(delta / (1000 * 60));
    delta -= minutes * 1000 * 60;
    var seconds = Math.floor(delta / 1000);

    // 更新 HTML
    document.getElementById("runningTime").innerHTML = "稳定运行 " + years + " 年 " + months + " 月 " + days + " 日 " + hours + " 时 " + minutes + " 分 " + seconds + " 秒";
}

// 页面加载完成时计算运行时间，并每秒更新一次
document.addEventListener('DOMContentLoaded', function () {
    calculateRunningTime();
    setInterval(calculateRunningTime, 1000); // 每秒更新一次
});