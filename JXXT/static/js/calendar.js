/**
 * Created by kylinhao on 2015/6.
 */
Date.prototype.isLeapYear = function () {
    return (0 == this.getYear() % 4 && ((this.getYear() % 100 != 0) || (this.getYear() % 400 == 0)));
}

Date.prototype.format = function (format) {
    var o = {
        "M+": this.getMonth() + 1, //month
        "d+": this.getDate(), //day
        "h+": this.getHours(), //hour
        "m+": this.getMinutes(), //minute
        "s+": this.getSeconds(), //second
        "q+": Math.floor((this.getMonth() + 3) / 3), //quarter
        "S": this.getMilliseconds() //millisecond
    }
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
            RegExp.$1.length == 1 ? o[k] :
                ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

function calendar() {
    var arr = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    var now = new Date();
    //当天是第几天
    var day = now.getDate();
    // 获取当天是周几
    var week = now.getDay();
    var month = now.getMonth();
    if (Date.prototype.isLeapYear != 0)
        arr[2] = 29;
    r = day % 7;
    if (r == 0)
        r = 7;
    // 得到星期一是周几
    var week1 = (week + 7 - (r - 1)) % 7;
    var table = document.getElementById("calendar-table");
    var name = document.getElementById("calendar-name");
    var time = document.getElementById("calendar-time");
    var newRow = table.insertRow(table.rows.length);
    for (var j = 0; j < week1; j++) {
        var cell = newRow.insertCell(newRow.cells.length);
        cell.innerHTML = ""
    }
    var i = 1;
    while (i <= arr[month]) {
        if (week1 != 7) {
            var cell = newRow.insertCell(newRow.cells.length);
            cell.innerHTML = i;
            //cell.style.fontSize ="19px"
            //cell.style.color = "gray"
            if (i == day) {
                cell.style.backgroundColor = "#66afe9"
                cell.style.color = "white"
            }
            week1++;
            i++;
        }
        else {
            week1 = 0;
            newRow = table.insertRow(table.rows.length);
        }
    }
    while (week1 < 7) {
        var cell = newRow.insertCell(newRow.cells.length);
        cell.innerHTML = "";
        week1++;
    }

    month = month + 1;
    name.innerHTML = month + "月日历";
    time.innerHTML = now.format("yyyy-MM-dd hh:mm:ss");
}