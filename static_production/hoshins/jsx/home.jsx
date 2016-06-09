$(function (){
    var submitButton = $("button");
    var req = undefined;
    $( "input" ).on("keyup", function() {
        var name = $( this ).val();

        if(name != "") {
            if(!_.isUndefined(req))
                req.abort();
            req = $.get("/teams", {name:name}).done(function(models) {
                if(models.length > 0)
                    submitButton.html("Join");
                else
                    submitButton.html("Create");
            });
        }
    });
});