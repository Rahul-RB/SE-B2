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

    // START: jqeury timeline calendar code
    $("#myTimeline").timeline({
        startDatetime: '2017-05-28',
        rangeAlign: 'center'
    });

    $("#myTimeline").on('afterRender.timeline', function(){
        // usage bootstrap's popover
        $('.timeline-node').each(function(){
            if ( $(this).data('toggle') === 'popover' ) {
                $(this).attr( 'title', $(this).text() );
                $(this).popover({
                    trigger: 'hover'
                });
            }
        });
    });
    // END: jqeury timeline calendar code

    // START: Popup defaults
    $.fn.popup.defaults.pagecontainer = '.popupClass';
    $('#basic').popup();
    $('#basic2').popup();

    // END : Popup defaults

    // START: Request Lab Test functionality
    $("#reqLabTestBtn").html("Request Lab Test");
    $("#reqLabTestBtn").on("click",function(argument){

    });
    // END : Request Lab Test functionality

    // START: Buy Medicine functionality
    $("#bookMedicineBtn").on("click",function(argument){
          
    });
    // END : Buy Medicine functionality

    // START : Following lines are used to control the 
    // Set reminder functionalities in tabs.
    $("#doctorReminderOptions").show();
    $("#medicineReminderOptions").hide();
    $("#labTestReminderOptions").hide();

    $("#doctorReminder").on("click", function(argument) {
        $("#searchTextBox").attr("placeholder","Search for Doctors");
        $("#medicineReminderOptions").hide();
        $("#labTestReminderOptions").hide();
    });
    $("#medicineReminder").on("click", function(argument) {
        $("#searchTextBox").attr("placeholder","Search for Pharmacies");
        $("#medicineReminderOptions").show();
        $("#labTestReminderOptions").hide();
    });
    $("#labTestReminder").on("click", function(argument) {
        $("#searchTextBox").attr("placeholder","Search for Labs");
        $("#labTestReminderOptions").show();
        $("#medicineReminderOptions").hide();
    });
    //END : Set Reminder tab functionalities.

    // START : jquery dropdown timepicker code.
    $('#doctorTimeScroll').timepicker({ 
            'scrollDefault': 'now' 
    });
    // END : jquery dropdown timepicker code.

    /* End Adding your javascript here */
});