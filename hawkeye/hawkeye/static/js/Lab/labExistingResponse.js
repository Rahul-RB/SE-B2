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
    $("#pres").hide();
    $('#viewPrescription').click(function(){
        if($(this).prop("checked") == true){
        /*alert("Checkbox is checked.");*/
            $("#pres").show();

        }
        else if($(this).prop("checked") == false){
        /*alert("Checkbox is unchecked.");*/
            $("#pres").hide();
        }
    });
    
    
    $('#seeResponse').click(function(){
        if($(this).prop("checked") == true){
            /*alert("Checkbox is checked.");*/
            $("#labResponse").show();
        }
        else if($(this).prop("checked") == false){
            /*alert("Checkbox is unchecked.");*/
            $("#labResponse").hide();
        }
    });
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
  
 

    /* End Adding your javascript here */
});
