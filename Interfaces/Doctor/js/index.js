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
    $('#notifications').hide();
    function toggleNotif(){
        console.log('pressed');
        $('#notifications').toggle("slow");
    }
    $("#notifContainerCloseBtn").on("click",function(){
        toggleNotif();
    });
    $("#notifToggler").on("click",function(){
        toggleNotif();
    });
    // $('#navbar-toggler').click(function(){
    //     console.log('pressed');
    //     $('#notifications').toggle("slow");
    // });
    /* End Adding your javascript here */
});
