/**
 * Created by kylin on 2015/7/2.
 */
// every page number n, i th page
$(document).ready(function () {
    create_button("table", 8, "btn-group")
    paging("table", 8, 1)
    $('button').on('click', function () {
        var text = $(this).text();
        var i = parseInt(text);
        paging("table", 8, i)
    });
});
function create_button(tableId, n, btnId) {
    var table = document.getElementById(tableId);
    len = table.rows.length;
    var btn = document.getElementById(btnId);
    var m_btn = Math.ceil(len / n);
    var html = ""
    for (var i = 1; i <= m_btn; i++) {
        html += "<button type='button' class='btn btn-default'>" + i + "</button>"
    }
    btn.innerHTML = html;
}
function paging(tableId, n, i) {
    var table = document.getElementById(tableId);
    var begin = (i - 1) * n ;
    var end = i * n;
    table.rows[0].style.display = "";
    for (var j = 1; j < table.rows.length; j++) {
        if (j > begin && j <= end) {
            table.rows[j].style.display = "";
        }
        else {
            table.rows[j].style.display = "none";
        }
    }
}
