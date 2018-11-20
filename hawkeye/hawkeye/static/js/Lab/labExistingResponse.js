$(document).ready(function () {

    /* Start Adding your javascript here */
    
    /*Setting up initial state of Prescription View to Hidden*/
    $("#pres").hide();

    /*Toggle Prescription View based on slider*/
    $('#viewPrescription').click(function(){
        if($(this).prop("checked") == true){
            $("#pres").show();

        }
        else if($(this).prop("checked") == false){
            $("#pres").hide();
        }
    });

    /* End Adding your javascript here */
});
