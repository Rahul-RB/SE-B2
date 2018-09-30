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
    $("#doctorReminderOptions").show();
    $("#medicineReminderOptions").hide();
    $("#labTestReminderOptions").hide();

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
    $('#doctorTimeScroll').timepicker({ 
            'scrollDefault': 'now' 
    });
    /* End Adding your javascript here */
});