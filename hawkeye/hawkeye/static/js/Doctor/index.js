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
    // START: jqeury timeline calendar code
    // $("#myTimeline").timeline({
    //     startDatetime: '2018-09-07',
    //     rangeAlign: 'center'
    // });

    // $("#myTimeline").on('afterRender.timeline', function(){
    //     // usage bootstrap's popover
    //     $('.timeline-node').each(function(){
    //         if ( $(this).data('toggle') === 'popover' ) {
    //             $(this).attr( 'title', $(this).text() );
    //             $(this).popover({
    //                 trigger: 'hover'
    //             });
    //         }
    //     });
    // });
    // END: jqeury timeline calendar code
    
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


    // START: meant for dynamic addition of rows in a table for symptoms and medicines
    $(".addCF").click(function(){
        $("#customFields").append('<tr valign="top"><th scope="row"><label for="customFieldName">Symptoms and Medicines </label></th><td><input type="text" class="code" id="customFieldName" name="customFieldName[]" value="" placeholder="Enter symptoms here...." /> &nbsp; <input type="text" class="code" id="customFieldValue" name="customFieldValue[]" value="" placeholder="Enter medicines here...." /> &nbsp;<input type="checkbox" value="M" >Morning</input>&nbsp;<input type="checkbox" value="A" >Afternoon </input>&nbsp;<input type="checkbox" value="N" > Night </input>&nbsp; <a href="javascript:void(0);" class="remCF">Remove</a></td></tr>');
    });

    $("#customFields").on('click','.remCF',function(){
        $(this).parent().parent().remove();
    });
    //END

    // START: meant for dynamic addition of rows in a table for labtests and description
    $(".addCF1").click(function(){
        $("#labFields").append('<tr valign="top"><th scope="row"></th><td><input type="text" class="code" id="labFieldName" name="customFieldName[]" value="" placeholder="Enter labtests here...." /> &nbsp; <input type="text" class="code" id="labFieldValue" name="customFieldValue[]" value="" placeholder="Enter description of tests here...." /> &nbsp;<a href="javascript:void(0);" class="remCF1">Remove</a></td></tr>');
    });

    $("#labFields").on('click','.remCF1',function(){
        $(this).parent().parent().remove();
    });
    //END


    /* Start Adding your javascript here */
    function getTodayDate(){
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();

        if(dd<10) {
            dd = '0'+dd
        } 

        if(mm<10) {
            mm = '0'+mm
        } 

        today = yyyy + '/' + mm + '/' + dd;
        return(today);
    }

    $("#calendar").fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,listWeek'
        },
        themeSystem:'bootstrap4',
        bootstrapFontAwesome: true,
        nowIndicator: true,
        // defaultDate: '2018-03-12',
        slotDuration: '00:30:00',
        defaultDate: getTodayDate(),
        height: function(){
            var height = $(window).height();
            var width = $(window).width();
            if(width<2560){
                return 400;    
            }
            else if(width<1440){
                return 400;    
            }
            else if(width<1024){
                return 480;    
            }
            else if(width<768){
                return 480;    
            }
            else if(width<425){
                return 360;                    
            }
            else if(width<375){
                return 360;                    
            }
            else if(width<320){
                return 310;                    
            }
        },
        defaultView: "listWeek",
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: [
            {
                title: 'All Day Event',
                start: '2018-10-12',
            },
            {
                title: 'Long Event',
                start: '2018-10-12',
                end: '2018-10-13'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2018-10-13T16:00:00'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2018-10-15T16:00:00'
            },
            {
                title: 'Conference',
                start: '2018-10-15',
                end: '2018-10-17'
            },
            {
                title: 'Meeting',
                start: '2018-10-15T10:30:00',
                end: '2018-10-16T12:30:00'
            },
            {
                title: 'Lunch',
                start: '2018-10-15T12:00:00'
            },
            {
                title: 'Meeting',
                start: '2018-10-17T14:30:00'
            },
            {
                title: 'Happy Hour',
                start: '2018-10-19T17:30:00'
            },
            {
                title: 'Dinner',
                start: '2018-10-21T20:00:00'
            },
        ]
    });
    // var someEvent1 = {
    //         title: 'Birthday Party',
    //         start: '2018-10-12T23:00:00'
    //     }
    // function temp(){
    //     var someEvent2 = {
    //             title: 'Click for Google',
    //             url: 'http://google.com/',
    //             start: '2018-10-12'
    //         }
    //     return someEvent2;
    // }
    // $("#calendar").fullCalendar("renderEvent",someEvent1,"stick");
    // $("#calendar").fullCalendar("renderEvent",temp(),"stick");


    // END: jqeury timeline calendar code




    // $('#navbar-toggler').click(function(){
    //     console.log('pressed');
    //     $('#notifications').toggle("slow");
    // });
    /* End Adding your javascript here */
    // function deleteRow(row) {
    //   var i = row.parentNode.parentNode.rowIndex;
    //   document.getElementById('POITable').deleteRow(i);
    // }


    // function insRow() {
    //   console.log('hi');
    //   var x = document.getElementById('POITable');
    //   var new_row = x.rows[1].cloneNode(true);
    //   var len = x.rows.length;
    //   new_row.cells[0].innerHTML = len;

    //   var inp1 = new_row.cells[1].getElementsByTagName('input')[0];
    //   inp1.id += len;
    //   inp1.value = '';
    //   var inp2 = new_row.cells[2].getElementsByTagName('input')[0];
    //   inp2.id += len;
    //   inp2.value = '';
    //   x.appendChild(new_row);
    // }
  
});
