/**
 * Created by kylin on 2015/6/18.
 */


$(document).ready(function () {

    //$(".main-show").height(document.body.scrollHeight - 160);
    $(".sidebar-menu").height(document.body.Height)
    //$(".main-menu li").mouseenter(function () {
    //    $(this).css("cursor", "pointer")
    //    var text = $(this).attr("class");
    //    $(this).addClass("highlight");
    //    if (text == "second-menu") {
    //        $(this).find('ul').slideDown("slow");
    //    }
    //});
    //$(".main-menu li").mouseleave(function () {
    //    $(this).removeClass("highlight");
    //    var text = $(this).attr("class");
    //    if (text == "second-menu") {
    //        $(this).find('ul').slideUp("slow");
    //    }
    //});
    $(".main-menu li").click(function () {
        $(this).css("cursor", "pointer")
        var text = $(this).attr("class");

        $(this).parent("ul").find("li").removeClass("highlight");

        $(".second-menu").find('ul').slideUp("fast");
        if (text == "second-menu") {
            $(this).addClass("highlight");
            $("#second-menu1").find('ul').slideUp("fast");
            $("#second-menu2").find('ul').slideUp("fast");
            $(this).find('ul').slideDown("fast");
        }
    });

});