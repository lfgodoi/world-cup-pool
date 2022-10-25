// Updating the simulated results
$(document).ready(function() {
    var audio = $("#audio");
    audio.trigger("play");
    $("#button-run").on("click", function() {
        request = $.ajax({
            url : "/run",
            type : "POST",
            data : {}
        });
        request.done(function(data) {
            $("#div-group-stage").html(data.content_group_stage);
            $("#div-knockout").html(data.content_knockout);
        });
    });
});

