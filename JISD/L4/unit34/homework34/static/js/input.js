$('.file').change(function () {
    let imgName = $('.file').val();
    let str = imgName.slice(12);
    // console.log(str);
    $('.a-upload').append('<p>' + str + '</p>');
})

//设置select的默认选中项颜色
$(function () {
    var unSelected = "#bababa";
    var selected = "#505050";
    $(function () {
        $("select").css("color", unSelected);
        $("option").css("color", selected);
        $("select").change(function () {
            var selItem = $(this).val();
            if (selItem == $(this).find('option:first').val()) {
                $(this).css("color", unSelected);
            } else {
                $(this).css("color", selected);
            }
        });
    })
})