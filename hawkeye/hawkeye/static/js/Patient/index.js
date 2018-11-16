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
    // START: jqeury timeline calendar code
    // $('#calendar').fullCalendar({
    //     // put your options and callbacks here
    // });
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,listWeek'
        },
        themeSystem:'bootstrap4',
        bootstrapFontAwesome: true,
        nowIndicator: true,
        // defaultDate: '2018-03-12',
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
        // eventMouseover: function(event) {
        //     $(this).qtip();
        // },
        // eventMouseout: function(event) {
        //     $(this).qtip().hide();
        // },
        // Don't render the modal on onclick
        // Keep the classes and divs attached in the get request itself
        // During the click, fetch data as per thing and display in modal.
        eventClick: function(event, element, view) {
            // element.qtip({
            //     content: event.subInfo
            // });
            if(event.hasOwnProperty("mainInfo"))
            {
                if(event.hasOwnProperty("subInfo"))
                {
                    var res = "<span class='mainInfo'>"+event.mainInfo+"</span>"+
                               "<span class='subInfo'>"+event.subInfo+"</span>";
                }
                else
                {
                    var res = "<span class='mainInfo'>"+event.mainInfo+"</span>";
                }
            }
            else if(event.hasOwnProperty("subInfo"))
            {
                var res = "<span class='subInfo'>"+event.subInfo+"</span>";
            }
            else
            {
                var res = "<span class='subInfo'></span>";
            }
            
            $(".fc-list-item").attr('data-toggle', 'modal');
            $(".fc-list-item").attr('data-target', '#commonModal');
            $(".fc-event-container").attr('data-toggle', 'modal');
            $(".fc-event-container").attr('data-target', '#commonModal');

            $("#commonModalBody").empty();
            $("#commonModalLongTitle").empty();
            $("#commonModalLongTitle").append("<div class='calendarEvent'>"+event.title+"</div>");
            $("#commonModalBody").append(res);

            switch(event.typeOfData)
            {
                case "OrderMedicine" :
                    var inpData = {
                        ID:event.ePrescriptionID
                    }
                    $.ajax({
                        url: 'getMedicineDetailsByEPrescriptionID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("Order data:",data);
                        $("#commonModalBody").append("\
                            <div><b>Symptoms:                  </b>"+data[0][0]+" </div>\
                            <div><b>Medicines Suggested:       </b>"+data[0][1]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });
                    break;

                case "LabVisit" :
                    var inpData = {
                        ID:event.labID,
                        accType:"Lab"
                    }
                    $.ajax({
                        url: 'getDetailsByID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("LabVisit data:",data);
                        $("#commonModalBody").append("\
                            <div><b>Lab ID:         </b>"+data[0][0]+" </div>\
                            <div><b>Lab Name:       </b>"+data[0][1]+" </div>\
                            <div><b>Address:        </b>"+data[0][2]+" </div>\
                            <div><b>Email:          </b>"+data[0][3]+" </div>\
                            <div><b>Phone NO:       </b>"+data[0][4]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });
                    break;

                case "DocVisit" :
                    var inpData = {
                        ID:event.doctorID,
                        accType:"Doctor"
                    }
                    $.ajax({
                        url: 'getDetailsByID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        // doctorID
                        // doctorName
                        // email
                        // dob
                        // address
                        // sex
                        // phoneNO
                        // designation
                        console.log("DocVisit data:",data);
                        $("#commonModalBody").append("\
                            <div><b>Doctor ID:     </b>"+data[0][0]+" </div>\
                            <div><b>Doctor Name:    </b>"+data[0][1]+" </div>\
                            <div><b>email:         </b>"+data[0][2]+" </div>\
                            <div><b>dob:           </b>"+data[0][3]+" </div>\
                            <div><b>address:       </b>"+data[0][4]+" </div>\
                            <div><b>sex:           </b>"+data[0][5]+" </div>\
                            <div><b>phoneNO:       </b>"+data[0][6]+" </div>\
                            <div><b>designation:   </b>"+data[0][7]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });

                    break; 
                default: break;
            }

        },
    });

    // END: jqeury timeline calendar code


    // Seven types of continuous fetch I've to do:
    //      1. Fetch all reminders - medicine, doc visit, lab test
    //      2. Fetch all doctor appointments
    //      3. Previous Prescriptions
    //      4. Lab Requests
    //      5. Lab Responses
    //      6. Medicine Requests
    //      7. Medicine Responses
    // On page load do:
    //   - Get all DoctorAppointment, *reminders
    //   - Get all Prescriptions and Lab Tests.
    //   - Load them into calendar.  

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

    // Get all CalendarReminderUpdate.
    // setInterval(function worker1() {
    //     $.get('patientCalendarReminderUpdate', function(data) {
    //         console.log("<GET:1> success",data);
    //     });
    // },10000);

    function getISO8601DateTime(date,time)
    {
        if(time.length==7)
        {
            return date+"T"+"0"+time;
        }
        else
        {
            return date+"T"+time;            
        }
    }
    (function worker1() {
        $.get('patientCalendarReminderUpdate', function(data) {
            console.log("<GET:1> success",data);

            $.each(data["TakeMedicine"], function(index, val) {
                var TakeMedicine = {
                    title: "Take Medicine",
                    start: getISO8601DateTime($(this)[3],$(this)[2]),
                    end: getISO8601DateTime($(this)[4],$(this)[2]),
                    subInfo: "Symptoms:"+$(this)[0]+"\n Medicine Suggested:"+$(this)[1],
                    typeOfData : "TakeMedicine"
                };
                console.log(TakeMedicine);
                $("#calendar").fullCalendar("renderEvent",TakeMedicine,"stick");
            });
            
            $.each(data["OrderMedicine"], function(index, val) {
                var OrderMedicine = {
                    title: "Order Medicine",
                    start: getISO8601DateTime($(this)[1],$(this)[2]),
                    subInfo: "Prescription ID:"+$(this)[0],
                    ePrescriptionID:$(this)[0],
                    typeOfData : "OrderMedicine"
                };
                console.log(OrderMedicine);
                $("#calendar").fullCalendar("renderEvent",OrderMedicine,"stick");
            });

            
            $.each(data["LabVisit"], function(index, val) {
                var LabVisit = {
                    title: "Lab Visit",
                    start: getISO8601DateTime($(this)[2],$(this)[3]),
                    subInfo: "LabID:"+$(this)[0]+"\tDocument ID:"+$(this)[1],
                    labID: $(this)[0],
                    typeOfData : "LabVisit"
                };
                console.log(LabVisit);
                $("#calendar").fullCalendar("renderEvent",LabVisit,"stick");
            });

            $.each(data["DocVisit"], function(index, val) {
                var DocVisit = {
                    title: "Doctor Visit",
                    start: getISO8601DateTime($(this)[1],$(this)[2]),
                    doctorID: $(this)[0],
                    typeOfData : "DocVisit"
                };
                console.log(DocVisit);
                $("#calendar").fullCalendar("renderEvent",DocVisit,"stick");
            });
        });
    })();

    // // Get all DoctorAppointment.
    (function worker2() {
        $.get('patientDoctorAppointment', function(data) {
            console.log("<GET:2> success",data);
            $.each(data, function(index, val) {
                var DocVisit = {
                    title: "Doctor Appointment",
                    start: getISO8601DateTime($(this)[1],$(this)[2]),
                    doctorID: $(this)[0],
                    typeOfData : "DocVisit"
                };
                console.log(DocVisit);
                $("#calendar").fullCalendar("renderEvent",DocVisit,"stick");                
            });
        });
    })();    
    // // Get all FetchPrescriptions.
    // setInterval(function worker3() {
    //     $.get('patientFetchPrescriptions', function(data) {
    //         console.log("<GET:3> success",data);
    //     });
    // },10000);
    (function worker3() {
        $.get('patientFetchPrescriptions', function(data) {
            console.log("<GET:3> success",data);
            
            // $("#prescriptionsViewCol").append("<div class='individualRowTwoItem list-group-item'>Prescription 1</div>");
            // $("#prescriptionData").text(data);
            $("#prescriptionsViewCol").empty();
            $("#prescriptionModalBody").empty();

            $.each(data, function(index, value) {
                /* iterate through array or object */
                $("#prescriptionsViewCol").append("\
                    <div class='individualRowTwoItem list-group-item' id='prescription"+index+"'data-toggle='modal' data-target='#prescriptionModal'>\
                        Prescription "+(index)+"\
                    </div>");
                $("#prescription"+index).each(function(index, el) {
                    $("#prescriptionModalLongTitle").text("Prescription "+(index));
                    $("#prescriptionModalBody").append("\
                        <div> <b> Prescription ID: </b>"+value[0]+"</div>\
                        <div> <b> Symptoms: </b>"+value[1]+"</div>\
                        <div> <b> Medicine Suggestion: </b>"+value[2]+"</div>\
                        <div> <b> Time To Take: </b>"+value[3]+"</div>\
                        <div> <b> Start Date: </b>"+value[4]+"</div>\
                    ");
                    // $(this).on('click', function(event) {
                    //     // $("#prescriptionModalBody").text("\n");
                    // });
                });
            });
        });
    })();

    // // Get all LabRequest.
    (function worker4() {
        $.get('patientLabRequest', function(data) {
            console.log("<GET:4> success",data);
        });
    })();
    
    // // Get all LabResponse.
    // setInterval(function worker5() {
    //     $.get('patientLabResponse', function(data) {
    //         console.log("<GET:5> success",data);
    //     });
    // },10000);
    
    // // Get all MedicineRequest.
    // setInterval(function worker6() {
    //     $.get('patientMedicineRequest', function(data) {
    //         console.log("<GET:6> success",data);
    //     });
    // },10000);
    
    // // Get all MedicineResponse.
    // setInterval(function worker7() {
    //     $.get('patientMedicineResponse', function(data) {
    //         console.log("<GET:7> success",data);
    //     });
    // },10000);
    

    // START: Popup defaults
    $.fn.popup.defaults.pagecontainer = '.popupClass';
    $('#basic').popup();
    $('#basic2').popup();
    $('#basic3').popup();

    var topRowBtnHeight = $("#mainButtons").css("height");
    $("#reqLabTestBtn").css("height",topRowBtnHeight);
    $("#bookMedicineBtn").css("height",topRowBtnHeight);
    $("#bookApptBtn").css("height",topRowBtnHeight);

    $("#reqLabTestBtn").on("click",function(event) {
        $(".popupSearchTextBox").val("");
        $(".selectedSearchID").val("");
    });
    $("#bookMedicineBtn").on("click",function(event) {
        $(".popupSearchTextBox").val("");
        $(".selectedSearchID").val("");
    });
    $("#bookApptBtn").on("click",function(event) {
        $(".popupSearchTextBox").val("");
        $(".selectedSearchID").val("");
    });

    // END : Popup defaults

    // START: Buy Medicine functionality
    // $("#bookMedicineBtn").on("click",function(argument){
        // Func 1: Early fetch doctors names as per customer's typing. -- make it such that any search can be invoked.
        // Func 2: Fetch times as per doctor suggested. Refresh this every 5 seconds.
        // Func 3: Poll Reminder tables and add them into calendar every 5 seconds.
        // Func 4: On page load, get all entries from DoctorAppointment table and load to calendar. Then call func3 periodically.
        // Step 1: Upon Doctor-Date-Time selection, make entry into DoctorAppointment table.
        // Step 2: Make an entry into DoctorReminder table. Let Func3 handle updation part.           
    // });
    // END : Buy Medicine functionality

    // START : Following lines are used to control the 
    // Set reminder functionalities in tabs.
    $("#doctorReminderOptions").show();
    $("#medicineReminderOptions").hide();
    $("#labTestReminderOptions").hide();

    $("#doctorReminder").on("click", function(argument) {
        $(".reminderSearchTextBox").attr("placeholder","Search for Doctors");
        $(".reminderSearchTextBox").attr("name","popupDoctorSearch");
        $("#doctorReminderMessage").show();
        $("#medicineReminderOptions").hide();
        $("#labTestReminderOptions").hide();
    });
    $("#medicineReminder").on("click", function(argument) {
        $(".reminderSearchTextBox").attr("placeholder","Search for Pharmacies");
        $(".reminderSearchTextBox").attr("name","popupMedicineSearch");
        $("#doctorReminderMessage").hide();
        $("#medicineReminderOptions").show();
        $("#labTestReminderOptions").hide();
    });
    $("#labTestReminder").on("click", function(argument) {
        $(".reminderSearchTextBox").attr("placeholder","Search for Labs");
        $(".reminderSearchTextBox").attr("name","popupLabSearch");
        $("#doctorReminderMessage").hide();
        $("#labTestReminderOptions").show();
        $("#medicineReminderOptions").hide();
    });
    //END : Set Reminder tab functionalities.

    // START : jquery dropdown timepicker code.
    // $('.timeScroller').each(function(index, el) {
    //     $(this).timepicker({ 
    //         'scrollDefault': 'now',
    //         'forceRoundTime': true,
    //         'timeFormat': 'H:i:s' 
    //     });
    // }); 
    // END : jquery dropdown timepicker code.


    // START : Search functionality
    function getResTypeByName(name) {
        if(name.search("Doctor")!=-1)
        {
            return "Doctor";
        }
        else if(name.search("Medicine")!=-1)
        {
            return "Medicine";
        }
        else if(name.search("Lab")!=-1)
        {
            return "Lab";
        }
    }

    $(".popupSearchTextBox").each(function(index, el){
        $(this).on('input', function(event) {
            var inpData = {
                inpText : $(this).val(),
                resType : getResTypeByName($(this).attr('name'))
            };
            console.log("$(this).attr('name'):",$(this).attr('name'));
            
            // Remove all children
            $("#popup"+inpData["resType"]+"SearchResults").empty();
            
            console.log(inpData)
            if(inpData["inpText"].length >= 3) // send request only when 3+ characters are typed
            {
                $.ajax({
                    url: 'commonSearch',
                    type: 'GET',
                    dataType: 'json',
                    data: inpData,
                })
                .done(function(data) {

                    if(!data.hasOwnProperty("data"))//make divs and put data
                    {
                        $.each(data, function(index, val) {
                            /* iterate through data */
                            $("#popup"+inpData["resType"]+"SearchResults").append("\
                                <div class='popupSearchResultsDiv'>\
                                    <div class='popupSearchResultsName'>"
                                        + val[0] +
                                    "</div>\
                                    <div class='popupSearchResultsID' hidden>"
                                        + val[1] +
                                    "</div>\
                                </div>\
                            ");
                            $(".popupSearchResultsDiv").on('click', function(event) {
                                /* Act on the event */
                                console.log("$('.popupSearchResultsName').text():",$(".popupSearchResultsName").text());
                                $(".popupSearchTextBox").val($(".popupSearchResultsName").text());
                                $(".selectedSearchID").val($(".popupSearchResultsID").text());
                                $("#popup"+inpData["resType"]+"SearchResults").empty();
                            }); 
                        });
                    }
                })
                .fail(function(err) {
                    console.log("error");
                    console.log(err);
                })
                .always(function() {
                    console.log("complete");
                });
                
            }
        });
    });
 

    // END : Search functionality

    // START : Popup Book button fucntionality -> Booking doctor appointment, buy medicines etc.
    function getInputTypeDateByID(ID){
        var date = new Date($("#"+ID).val());
        day = date.getDate();
        month = date.getMonth() + 1;
        year = date.getFullYear();
        return([year, month, day].join('-'));
    }

    function diffBetweenArrs (a1, a2) {

        var a = [], diff = [];
        for (var i = 0; i < a1.length; i++) {
            a[a1[i]] = true;
        }

        for (var i = 0; i < a2.length; i++) {
            if (a[a2[i]]) {
                delete a[a2[i]];
            } else {
                a[a2[i]] = true;
            }
        }

        for (var k in a) {
            diff.push(k);
        }

        return diff;
    }

    var allTimeSlots = ["00:00:00", "00:30:00", "01:00:00", "01:30:00", 
                        "02:00:00", "02:30:00", "03:00:00", "03:30:00", 
                        "04:00:00", "04:30:00", "05:00:00", "05:30:00", 
                        "06:00:00", "06:30:00", "07:00:00", "07:30:00", 
                        "08:00:00", "08:30:00", "09:00:00", "09:30:00", 
                        "10:00:00", "10:30:00", "11:00:00", "11:30:00", 
                        "12:00:00", "12:30:00", "13:00:00", "13:30:00", 
                        "14:00:00", "14:30:00", "15:00:00", "15:30:00", 
                        "16:00:00", "16:30:00", "17:00:00", "17:30:00", 
                        "18:00:00", "18:30:00", "19:00:00", "19:30:00", 
                        "20:00:00", "20:30:00", "21:00:00", "21:30:00", 
                        "22:00:00", "22:30:00", "23:00:00", "23:30:00"];

    function setAvailableTimeSlots(doctorID, inpDate)
    {
        var inpData = {
            doctorID : doctorID,
            inpDate : inpDate
        };
        $.ajax({
            url: 'getAvailableTimeSlots',
            type: 'GET',
            dataType: 'json',
            data: inpData,
        })
        .done(function(data) {
            var dataToArr = [];
            $.each(data, function(index, val) {
                dataToArr.push(val);
            });
            var res = diffBetweenArrs(allTimeSlots,dataToArr);
            console.log("res:",res);
        
            $.each(res, function(index, val) {
                $(".timeScroller").append("<option>"+val+"</option>");
            });
        })
        .fail(function(err) {
            console.log("error");
            console.log(err);
        })
        .always(function() {
            console.log("complete");
        });
    }


    // For doctor appt booking:
    $("#popupDoctorDate").on('blur', function(event) {
        //might need to clear old doctorID and inpDate

        var doctorID = $("#selectedDoctorID").val();
        var inpDate = getInputTypeDateByID("popupDoctorDate");
        setAvailableTimeSlots(doctorID,inpDate);
    });

    $("#doctorApptBookBtn").on('click',function(event) {
        event.preventDefault();
        /* Act on the event */
        var doctorID = $("#selectedDoctorID").val();
        var inpDate = getInputTypeDateByID("popupDoctorDate");
        
        var payload = {
            doctorID : doctorID,
            apptDate : inpDate,
            apptTime : $("#popupDoctorTime").find(":selected").text() // must be 24 hrs, like 18:30
        }
        var jsonPayload = JSON.stringify(payload);
        console.log(jsonPayload)

        $.ajax({
            url: 'patientDoctorAppointment',
            type: 'POST',
            dataType: 'json',
            data: jsonPayload,
            contentType:"application/json; charset=UTF-8"
        })
        .done(function(data) {
            console.log("success");
            console.log(data);
            $("#doctorBookMessage").append("\
                <div class='alert alert-success alert-dismissible fade show' role='alert'>\
                    <strong>Appointment booked successfully!</strong><br> Your calendar will be updated soon.\
                    <button type='button' class='close' data-dismiss='alert' aria-label='Close'>\
                        <span aria-hidden='true'>&times;</span>\
                    </button>\
                </div>\
            ");
        })
        .fail(function(err) {
            console.log("error");
            console.log(err);
            $("#doctorBookMessage").append("\
                <div class='alert alert-danger alert-dismissible fade show' role='alert'>\
                    <strong>Server Error:</strong>"+err+".\
                    <button type='button' class='close' data-dismiss='alert' aria-label='Close'>\
                        <span aria-hidden='true'>&times;</span>\
                    </button>\
                </div>\
            ");
        })
        .always(function() {
            console.log("complete");
        });
        
    });

    $("#labBookBtn").on('click',function(event) {
        event.preventDefault();
        /* Act on the event */

        var payload = {
            labID : $("#selectedLabID").val(),
            // apptDate : getInputTypeDateByID("popupLabDate"),
        }
        var jsonPayload = JSON.stringify(payload);
        console.log(jsonPayload)

        $.ajax({
            url: 'patientLabRequest',
            type: 'POST',
            dataType: 'json',
            data: jsonPayload,
            contentType:"application/json; charset=UTF-8"
        })
        .done(function(data) {
            console.log("success");
            console.log(data);
            $("#labBookMessage").append("\
                <div class='alert alert-success alert-dismissible fade show' role='alert'>\
                    <strong>Lab request sent successfully!</strong><br> Your calendar will be updated soon.\
                    <button type='button' class='close' data-dismiss='alert' aria-label='Close'>\
                        <span aria-hidden='true'>&times;</span>\
                    </button>\
                </div>\
            ");
        })
        .fail(function(err) {
            console.log("error");
            console.log(err);
            $("#labBookMessage").append("\
                <div class='alert alert-danger alert-dismissible fade show' role='alert'>\
                    <strong>Server Error:</strong>"+err+".\
                    <button type='button' class='close' data-dismiss='alert' aria-label='Close'>\
                        <span aria-hidden='true'>&times;</span>\
                    </button>\
                </div>\
            ");
        })
        .always(function() {
            console.log("complete");
        });  
    });
    
    $("#medicineBookBtn").on('click',function(event) {
        event.preventDefault();
        /* Act on the event */

        var payload = {
            labID : $("#selectedMedicineID").val(),
            // apptDate : getInputTypeDateByID("popupMedicineDate"),
        }
        var jsonPayload = JSON.stringify(payload);
        console.log(jsonPayload)

        $.ajax({
            url: 'patientMedicineRequest',
            type: 'POST',
            dataType: 'json',
            data: jsonPayload,
            contentType:"application/json; charset=UTF-8"
        })
        .done(function(data) {
            console.log("success");
            console.log(data);
            $("#labBookMessage").append("\
                <div class='alert alert-success alert-dismissible fade show' role='alert'>\
                    <strong>Medicine request sent successfully!</strong><br> Your calendar will be updated soon.\
                    <button type='button' class='close' data-dismiss='alert' aria-label='Close'>\
                        <span aria-hidden='true'>&times;</span>\
                    </button>\
                </div>\
            ");
        })
        .fail(function(err) {
            console.log("error");
            console.log(err);
            $("#labBookMessage").append("\
                <div class='alert alert-danger alert-dismissible fade show' role='alert'>\
                    <strong>Server Error:</strong>"+err+".\
                    <button type='button' class='close' data-dismiss='alert' aria-label='Close'>\
                        <span aria-hidden='true'>&times;</span>\
                    </button>\
                </div>\
            ");
        })
        .always(function() {
            console.log("complete");
        });
    });
    
        
    // END : Popup Book button fucntionality -> Booking doctor appointment, buy medicines etc.
    

    // Seven types of continuous fetch I've to do:
    //      1. Fetch all reminders - medicine, doc visit, lab test
    //      2. Fetch all doctor appointments
    //      3. Previous Prescriptions
    //      4. Lab Requests
    //      5. Lab Responses
    //      6. Medicine Requests
    //      7. Medicine Responses
    
    // // START : 1. EventSource : Reminder fetch and update calendar
    // var pcr = new EventSource("/patientCalendarReminderUpdate");
    // pcr.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES1> PCR success:",event.data);
    // });

    // pcr.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // pcr.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 1. EventSource : Reminder fetch and update calendar

    // // START : 2. EventSource : Appointment fetch and update calendar
    // var pda = new EventSource("/patientDoctorAppointment");
    // pda.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES2> PDA success:",event.data);
    // });

    // pda.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // pda.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 2. EventSource : Appointment fetch and update calendar

    // // START : 3. EventSource : Prescription fetch and update calendar
    // var pfp = new EventSource("/patientFetchPrescriptions");
    // pfp.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES3> PFP success:",event.data);
    // });

    // pfp.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // pfp.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 3. EventSource : Prescription fetch and update calendar

    // // START : 4. EventSource : LabRequest fetch and update calendar
    // var plReq = new EventSource("/patientLabRequest");
    // plReq.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES4> PLReq success:",event.data);
    // });

    // plReq.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // plReq.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 4. EventSource : LabRequest fetch and update calendar

    // // START : 5. EventSource : LabRequest fetch and update calendar
    // var plResp = new EventSource("/patientLabResponse");
    // plResp.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES5> PLResp success:",event.data);
    // });

    // plResp.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // plResp.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 5. EventSource : LabRequest fetch and update calendar

    // // START : 6. EventSource : MedicineRequest fetch and update calendar
    // var pmReq = new EventSource("/patientMedicineRequest");
    // pmReq.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES6> PMReq success:",event.data);
    // });

    // pmReq.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // pmReq.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 6. EventSource : MedicineRequest fetch and update calendar

    // // START : 7. EventSource : MedicineResponse fetch and update calendar
    // var pmResp = new EventSource("/patientMedicineResponse");
    // pmResp.addEventListener("someEvent",function (event) {
    //     // TODO: FORMAT THIS CRAP INTO FUCKING HTML
    //     console.log("<ES7> PMResp success:",event.data);
    // });

    // pmResp.onmessage = function(event) {
    //     console.log(event.data);
    // };
    // pmResp.onerror = function(event) {
    //     console.log(event.data);
    // };
    // // END : 7. EventSource : MedicineResponse fetch and update calendar


    /* End Adding your javascript here */
});