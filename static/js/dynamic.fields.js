$(document).ready(function() {
    var button_x_Add = $("#add-button");
    var button_x_Remove = $("#remove-button");
    var class_x_Name = ".dynamic-field";
    var count_x = 0;
    var field_x = "";
    var maxFields_x = 10;
    function totalFields() {
    return $(class_x_Name).length;
}
    function addNewField() {
    count_x = totalFields() + 1;
    field_x = $("#dynamic-field-1").clone();
    field_x.attr("id", "dynamic-field-" + count_x);
    field_x.children("label").text("Column " + count_x);
    field_x.find("input").val("");
    field_x.find("#order-field").val("" + count_x);
    $(class_x_Name + ":last").after($(field_x));
}
    function removeLastField() {
    if (totalFields() > 1) {
    $(class_x_Name + ":last").remove();
}
}
    function enableButtonRemove() {
    if (totalFields() === 2) {
    button_x_Remove.removeAttr("disabled");
    button_x_Remove.addClass("shadow-sm");
}
}
    function disableButtonRemove() {
    if (totalFields() === 1) {
    button_x_Remove.attr("disabled", "disabled");
    button_x_Remove.removeClass("shadow-sm");
}
}
    function disableButtonAdd() {
    if (totalFields() === maxFields_x) {
    button_x_Add.attr("disabled", "disabled");
    button_x_Add.removeClass("shadow-sm");
}
}
    function enableButtonAdd() {
    if (totalFields() === (maxFields_x - 1)) {
    button_x_Add.removeAttr("disabled");
    button_x_Add.addClass("shadow-sm");
}
}
    button_x_Add.click(function() {
    addNewField();
    enableButtonRemove();
    disableButtonAdd();
});
    button_x_Remove.click(function() {
    removeLastField();
    disableButtonRemove();
    enableButtonAdd();
});
});