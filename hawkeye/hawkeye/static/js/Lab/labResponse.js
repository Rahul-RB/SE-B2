$(document).ready(function () {
    /* Do not disturb below lines */
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#dismiss, .overlay').on('click', function () {
        $('#sidebar').removeClass('active');
        $('.overlay').removeClass('active');
    });

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').addClass('active');
        $('.overlay').addClass('active');
        $('.navbar-collapse.in').toggleClass('in');
        // $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });

    $('#navbarCollapseBtn').on('shown.bs.collapse', function () {
        console.log("Toggled!");
        $("#navbarCollapseBtnLink").children('.fa-align-justify').remove();
    
        $("#navbarCollapseBtnLink").append("<span><i class='fas fa-sliders-h'></i>&nbsp;&nbsp;&nbsp;Options</span>");
        $("#navbarCollapseBtnEnv").append("&nbsp;&nbsp; Messages");
        $("#navbarCollapseBtnBell").append("&nbsp;&nbsp; Notifications");
        $("#navbarCollapseBtnUser").append("&nbsp;&nbsp; You");
    
    });
    /* Do not disturb above lines */
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
