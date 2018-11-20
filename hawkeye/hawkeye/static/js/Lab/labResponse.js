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

    /*Toggle the view of response*/
    $('#writeResponse').click(function(){
        if($(this).prop("checked") == true){
            $("#labform").show();
        }
        else if($(this).prop("checked") == false){
            $("#labform").hide();
        }
    });

    /*Function to fetch current date*/
   function SetDate()
   {
       var date = new Date();
       var day = date.getDate();
       var month = date.getMonth() + 1;
       var year = date.getFullYear();
       if (month < 10) month = "0" + month;
       if (day < 10) day = "0" + day;
       var today = year + "-" + month + "-" + day;
       return today;
   }
   
   document.getElementById('date').value = SetDate();


    /* End Adding your javascript here */
});
