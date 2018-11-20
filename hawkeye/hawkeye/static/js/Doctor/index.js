// for updating the sidebar and navigation bar

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


    var timingVar=2; // because epresription.html has  timing1 used.
    // START: meant for dynamic addition of rows in a table for symptoms and medicines
    $(".addCF").click(function(){
        $("#customFields").append("\
            <tr valign='top'>\
                <th scope='row'>\
                </th>\
                <td>\
                    <input type='text' class='code' id='customSymptomName' name='customSymptomName' value='' placeholder='Enter symptoms here....' /> &nbsp; \
                    <input type='text' class='code' id='customMedicineValue' name='customMedicineValue' value='' placeholder='Enter medicines here....' /> &nbsp;\
                    <input type='checkbox' name='timing"+timingVar+"' value='9:00:00' >Morning</input>&nbsp;\
                    <input type='checkbox' name='timing"+timingVar+"' value='13:00:00' >Afternoon </input>&nbsp;\
                    <input type='checkbox' name='timing"+timingVar+"' value='19:00:00' > Night </input>&nbsp;\
                    <a href='javascript:void(0);' class='remCF'>Remove</a>\
                </td>\
            </tr>");
        timingVar++;
    });

    $("#customFields").on('click','.remCF',function(){
        $(this).parent().parent().remove();
    });
    //END

    // START: meant for dynamic addition of rows in a table for labtests and description
    $(".addCF1").click(function(){
        $("#labFields").append('<tr valign="top"><th scope="row"></th><td><input type="text" class="code" id="labTestTypeName" name="labTestTypeName" value="" placeholder="Enter labtests here...." /> &nbsp; <input type="text" class="code" id="labTestDescriptionValue" name="labTestDescriptionValue" value="" placeholder="Enter description of tests here...." /> &nbsp;<a href="javascript:void(0);" class="remCF1">Remove</a></td></tr>');
    });

    $("#labFields").on('click','.remCF1',function(){
        $(this).parent().parent().remove();
    });
    //END


    /* START: calendar utility functions like getTodayDate */
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

    // END

    // START: Calendar updation with basic UI

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

    // END
    
    // START: Check history of number of patients seen for Doctor and plot a line chart

    $("#doctorHistoryBtn").on("click", function (event) {
        var inpData = {
            searchBy : $("#date-input").val(),
            
        };
        $.ajax({
            url: 'checkDoctorsHistory',
            type: 'GET',
            dataType: 'json',
            data: inpData,
        })
        .done(function(data) {
            console.log(data);
            
            console.log(data["countPatientsMonth"]);
            console.log(data["countPatientsToday"]);
            console.log(data["monthWiseDataThatYear"][11]);
            $("#analyticsDiv").append("<div> Total Patients seen today is " + data["countPatientsToday"] + "</div>" );
            $("#analyticsDiv").append("<div> Total Patients seen for the selected month is " + data["countPatientsMonth"] + "</div>");
            $("#analyticsDiv").append("<div> Total Patients seen for the selected year is " + data["countPatientsYear"] + "</div>");
            
            var line_ctx = document.getElementById('lineChart').getContext('2d');
            var chart = new Chart(line_ctx, {
                  type: 'line',
                  data: {
                      labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                      datasets: [{
                          label: "Frequency of Patients through the Year",
                          backgroundColor: 'rgb(255, 99, 132)',
                          borderColor: 'rgb(255, 99, 132)',
                          data: data["monthWiseDataThatYear"], // put the frequency of each month list here
                      }]
                  },

                  // Configuration options go here
                  options: {
                      responsive: true
                  }
            });
            
            
            $("#lineChart").fadeIn();

        })
        .fail(function(err) {
            console.log("error");
            console.log(err);
        })
        .always(function() {
            console.log("complete");
        });
    })

    // END

    // START: Search bar for Patient's History
    $("#patientIDSeachBtn").on("click",function (event) {
        var inpData = {
            patientID : $("#patientIDInp").val()
        };

        $.ajax({
            url: '/getDetailsByID',
            type: 'GET',
            dataType: 'json',
            data: {"ID": $("#patientIDInp").val(), "accType": "Patient"}
        })
        .done(function(data) {
            console.log(data[0]);
            $('#patient-identity li').remove();
            $('#patient-identity').append("<li class='list-group-item'><strong>Name:  <span class='badge' style='background: white;'>" + data[0][1] + "  </span></strong></li>");
            $("#patient-identity").append("<li class='list-group-item'><strong>Gender:  <span class='badge' style='background: green; color:white;'>" + data[0][5] + "  </span></strong></li>");
            $("#patient-identity").append("<li class='list-group-item'><strong>Date of Birth:  <span class='badge' style='background: white;'>" + data[0][3] + "  </span></strong></li>");
        })
        .fail(function(err) {
            console.log("error in fetching details");
            console.log(err);
        });

        $.ajax({
            url: 'searchPatientHistory',
            type: 'GET',
            dataType: 'json',
            data: inpData,
        })
        .done(function(data) {
            
            console.log("Success");
            $('#patient-details li').remove();
            // console.log(data);

            var spans = null;
            $.each(data,function(index,value){
                
                console.log(value);

                $("#patient-details").append("<li class='list-group-item' style='margin-top:10px;'><strong>PrescriptionID:  </strong><span class='badge' style='background: skyblue; margin-left:2px;'>" + value["ePrescriptionID"] + "</span></li>");

                spans = "";
                $.each(value["symptoms"],function (index,value) {
                    spans += "<span class='badge' style='background: pink; margin-left:2px;'>" + value + "</span>";
                });
                $("#patient-details").append("<li class='list-group-item'><strong>Symptoms:  </strong>" + spans + "</li>");

                spans = "";
                $.each(value["medicineSuggestion"],function (index,value) {
                   spans +=  "<span class='badge' style='background: lightgreen; margin-left:2px;'>" + value + "</span>";
                });
                $("#patient-details").append("<li class='list-group-item'><strong>Medicines:  </strong>" + spans + "</li>");

                spans = "";
                $.each(value["testType"],function (index,value) {
                   spans += "<span class='badge' style='background: orange; margin-left:2px;'>" + value + "</span>";
                });
                $("#patient-details").append("<li class='list-group-item'><strong>Lab Tests:  </strong>" + spans + "</li>");

                spans = "";
                $.each(value["description"],function (index,value) {
                    spans += "<span class='badge' style='border: 1px solid black; margin-left:2px;'>" + value + "</span>";
                });
                $("#patient-details").append("<li class='list-group-item'><strong>Description:  </strong>" + spans + "</li>");

            });
        })
        .fail(function(err) {
            console.log("error");
            console.log(err);
        })
        .always(function() {
            console.log("complete");
        });
    })
});

    // END
