$(document).ready(function () {
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
        // Don't render the modal on onclick
        // Keep the classes and divs attached in the get request itself
        // During the click, fetch data as per thing and display in modal.
        eventClick: function(event, element, view) {
            // Since many events types are there, it's important to distinuish
            // them via property types they've. 
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
            
            // Add targets of these calendar event divs to a common modal.
            // Thus clicking them invokes this event (eventClick) and then
            // invoked bootstrap modal target which shows the modals. 
            $(".fc-list-item").attr('data-toggle', 'modal');
            $(".fc-list-item").attr('data-target', '#commonModal');
            $(".fc-event-container").attr('data-toggle', 'modal');
            $(".fc-event-container").attr('data-target', '#commonModal');

            // Ensure previously clicked modals data in calendars are cleared
            // before the next is clicked.
            $("#commonModalBody").empty();
            $("#commonModalLongTitle").empty();
            $("#commonModalLongTitle").append("<div class='calendarEvent'>"+
                                                event.title+"</div>");
            $("#commonModalBody").append(res);

            switch(event.typeOfData)
            {
                // If the event type was OrderMedicine then fetch the 
                // corresponding Data for the prescription : The symptoms and
                // medicines suggested for the same.
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
                            <div><b>Symptoms:           </b>"+data[0][0]+" </div>\
                            <div><b>Medicines Suggested:</b>"+data[0][1]+" </div>\
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

                // If the event type was LabVisit then fetch the 
                // corresponding Data for the visit : The lab details.
                // The user can view his lab requests to see what lab document
                // corresponds to this visit.
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

                // If the event type was DocVisit then fetch the 
                // corresponding Data for the visit : The doctor details.
                // The user can view his doctor details.
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
    //   - Then fetch all from 3-7.  


    // Function usage: Get date (yyyy/mm/dd) and time (hh:mm:ss) and convert it 
    // into ISO-8601 format ($dateT$time).
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
    
    // Function usage: Get all types of data that's required to be updated in 
    // calendar. These are 4 types of events to be updated in calendar: 
    //      - OrderMedicine
    //      - TakeMedicine
    //      - DocVisit
    //      - LabVisit
    // The AJAX call to patientCalendarReminderUpdate returns a JSON with
    // keys as 4 events. The values are an array of values, each depending on
    // data sent by backend.

    (function worker1() {
        $.get('patientCalendarReminderUpdate', function(data) {
            console.log("<GET:1> success",data);

            $.each(data["TakeMedicine"], function(index, val) {
                var TakeMedicine = {
                    title: "Take Medicine",
                    start: getISO8601DateTime($(this)[3],$(this)[2]),
                    end: getISO8601DateTime($(this)[4],$(this)[2]),
                    subInfo: "<b>Symptoms:</b>"+$(this)[0]+"<br> <b>Medicine Suggested:</b>"+$(this)[1],
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
    
    // Get all DoctorAppointment.
    // Function usage: Get all Doctor Appointments for the patient that's been 
    // booked on a earlier date by the same patient.
    // The AJAX call to patientDoctorAppointment returns a JSON with
    // keys as integer, each integer representing one [appointment]. 
    // The values are an array of values corresponding to the appointment, which
    // depends on the backend schema.
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
    
    // Get all FetchPrescriptions.
    // Function usage: Get all Prescriptions for the patient that's been 
    // issued on a earlier date by some doctor.
    // The AJAX call to patientFetchPrescriptions returns a JSON with
    // keys as integer, each integer representing one [prescription]. 
    // The values are an array of values corresponding to the appointment, which
    // depends on the backend schema.
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
                $("#prescription"+index).on("click",function(event) {
                    // $("#prescriptionsViewCol").empty();
                    $("#prescriptionModalBody").empty();
                    $("#prescriptionModalLongTitle").text("Prescription "+(index));
                    $("#prescriptionModalBody").append("\
                        <div> <b> Prescription ID: </b>"+value[0]+"</div>\
                        <div> <b> Symptoms: </b>"+value[1]+"</div>\
                        <div> <b> Medicine Suggestion: </b>"+value[2]+"</div>\
                        <div> <b> Time To Take: </b>"+value[3]+"</div>\
                        <div> <b> Start Date: </b>"+value[4]+"</div>\
                    ");
                });
            });
        });
    })();

    // Get all LabRequest.
    // Function usage: Get all Lab Requests for the patient that's been 
    // made by same patient using a lab document issued on a earlier date by 
    // some doctor.
    // The AJAX call to patientLabRequest returns a JSON with keys as integer, 
    // each integer representing one [LabRequest]. 
    // The values are an array of values corresponding to the appointment, which
    // depends on the backend schema.
    (function worker4() {
        $.get('patientLabRequest', function(data) {
            console.log("<GET:4> success",data);
            $("#labReqDiv").empty();
            $("#labReqModalBody").empty();

            $.each(data, function(index, value) {
                /* iterate through array or object */
                $("#labReqDiv").append("\
                    <div class='individualRowTwoItem list-group-item' id='labReq"+index+"'data-toggle='modal' data-target='#labReqModal'>\
                        Request "+(index)+"\
                    </div>");
                $("#labReq"+index).each(function(index, el) {
                    $("#labReqModalLongTitle").text("Request "+(index));
                    $("#labReqModalBody").append("\
                        <div> <b> Test Type : </b>"+value[2]+"</div>\
                        <div> <b> Test Details : </b>"+value[3]+"</div>\
                    ");

                    var inpData = {
                        ID:value[0],
                        accType:"Doctor"
                    }
                    $.ajax({
                        url: 'getDetailsByID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("DocVisit data:",data);
                        $("#labReqModalBody").append("\
                            <div><b> Issued by Doctor ID : </b>"+value[0]+"</div>\
                            <div style='margin-left:20px'><b>Doctor ID:     </b>"+data[0][0]+" </div>\
                            <div style='margin-left:20px'><b>Doctor Name:    </b>"+data[0][1]+" </div>\
                            <div style='margin-left:20px'><b>email:         </b>"+data[0][2]+" </div>\
                            <div style='margin-left:20px'><b>dob:           </b>"+data[0][3]+" </div>\
                            <div style='margin-left:20px'><b>address:       </b>"+data[0][4]+" </div>\
                            <div style='margin-left:20px'><b>sex:           </b>"+data[0][5]+" </div>\
                            <div style='margin-left:20px'><b>phoneNO:       </b>"+data[0][6]+" </div>\
                            <div style='margin-left:20px'><b>designation:   </b>"+data[0][7]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });

                    var inpData = {
                        ID:value[1]
                    };
                    // Fetch Prescription details for which the lab document
                    // was issued. 
                    $.ajax({
                        url: 'getMedicineDetailsByEPrescriptionID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("Order data:",data);
                        $("#labReqModalBody").append("\
                            <div><b> Issued for Prescription : </b>"+value[1]+"</div>\
                            <div style='margin-left:20px'><b>Symptoms:                  </b>"+data[0][0]+" </div>\
                            <div style='margin-left:20px'><b>Medicines Suggested:       </b>"+data[0][1]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });

                });
            });            
        });
    })();
    
    // Get all LabResponse.
    // Function usage: Get all Lab Responses for the patient that's been 
    // made by some lab using a lab document issued for request on a earlier 
    // date by same patient.
    // The AJAX call to patientLabResponse returns a JSON with keys as integer, 
    // each integer representing one [LabResponse]. 
    // The values are an array of values corresponding to the appointment, which
    // depends on the backend schema.
    (function worker5() {
        $.get('patientLabResponse', function(data) {
            console.log("<GET:5> success",data);

            $("#labRespDiv").empty();
            $("#labRespModalBody").empty();

            $.each(data, function(index, value) {
                /* iterate through array or object */
                $("#labRespDiv").append("\
                    <div class='individualRowTwoItem list-group-item' id='labResp"+index+"'data-toggle='modal' data-target='#labRespModal'>\
                        Response "+(index)+"\
                    </div>");
                $("#labResp"+index).on("click",function(event) {
                    $("#labRespModalBody").empty();
                    
                    $("#labRespModalLongTitle").text("Response "+(index));
                    $("#labRespModalBody").append("\
                        <div> <b> Result Link : </b><a href='"+value[2]+"'> Click Here </a></div>\
                        <div> <b> Result Details : </b>"+value[3]+"</div>\
                        <div> <b> Response Date and Time : </b>"+value[4]+"</div>\
                        <div> <b> Report ID : </b>"+value[0]+"</div>\
                    ");

                    var inpData={
                        ID:value[1]
                    };
                    // Fetch Lab request document details
                    $.ajax({
                        url: 'getELabRequestDocumentByID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("Order data:",data);
                        $("#labRespModalBody").append("\
                            <div><b> Issued for Lab Request Document : </b>"+data[0][0]+"</div>\
                            <div style='margin-left:20px'><b>Test Type : </b>"+data[0][4]+" </div>\
                            <div style='margin-left:20px'><b>Test Description : </b>"+data[0][5]+" </div>\
                            <div style='margin-left:20px'><b>Was Issued by Doctor : </b>"+data[0][1]+" </div>\
                            <div style='margin-left:20px'><b>Was Issued for Prescription : </b>"+data[0][2]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });                    
                });
            });
        });
    })();
    
    // Get all MedicineRequest.
    // Function usage: Get all Medicine Requests for the patient that's been 
    // made by same patient using a prescription issued on a earlier date by 
    // some doctor.
    // The AJAX call to patientMedicineRequest returns a JSON with keys as 
    // integer, each integer representing one [MedicineRequest]. 
    // The values are an array of values corresponding to the appointment, which
    // depends on the backend schema.
    (function worker6() {
        $.get('patientMedicineRequest', function(data) {
            console.log("<GET:6> success",data);
            $("#medReqDiv").empty();
            $("#medReqModalBody").empty();
            $.each(data, function(index, value) {
                /* iterate through array or object */
                $("#medReqDiv").append("\
                    <div class='individualRowTwoItem list-group-item' id='medReq"+index+"'data-toggle='modal' data-target='#medReqModal'>\
                        Request "+(index)+"\
                    </div>");
                $("#medReq"+index).on("click",function(event) {
                    $("#medReqModalBody").empty();
                    $("#medReqModalLongTitle").text("Request "+(index));
                    $("#medReqModalBody").append("\
                        <div><b> Delivery Time : </b>"+value[3]+"</div>\
                    ");

                    var inpData={
                        ID:value[2],
                        accType:"Pharmacy"
                    };
                    // Fetch Lab request document details
                    $.ajax({
                        url: 'getDetailsByID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("Order data:",data);
                        $("#medReqModalBody").append("\
                            <div><b> Issued to Pharmacy : </b>"+value[2]+"</div>\
                            <div style='margin-left:20px'><b>Pharmacy Name : </b>"+data[0][1]+" </div>\
                            <div style='margin-left:20px'><b>Address : </b>"+data[0][2]+" </div>\
                            <div style='margin-left:20px'><b>Phone No : </b>"+data[0][3]+" </div>\
                            <div style='margin-left:20px'><b>Email : </b>"+data[0][4]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });                    
                });
            });
        });
    })();
    
    // // Get all MedicineResponse.
    // Function usage: Get all Medicine Responses for the patient that's been 
    // made by same patient using a prescription issued on a earlier date by 
    // some doctor.
    // The AJAX call to patientMedicineResponse returns a JSON with keys as 
    // integer, each integer representing one [MedicineResponse]. 
    // The values are an array of values corresponding to the appointment, which
    // depends on the backend schema.

    (function worker7() {
        $.get('patientMedicineResponse', function(data) {
            console.log("<GET:7> success",data);
            
            $("#medRespDiv").empty();
            $("#medRespModalBody").empty();

            $.each(data, function(index, value) {
                /* iterate through array or object */
                $("#medRespDiv").append("\
                    <div class='individualRowTwoItem list-group-item' id='medResp"+index+"'data-toggle='modal' data-target='#medRespModal'>\
                        Responses "+(index)+"\
                    </div>");
                $("#medResp"+index).on("click",function(event) {
                    $("#medRespModalBody").empty();
                    $("#medRespModalLongTitle").text("Responses "+(index));
                    $("#medRespModalBody").append("\
                        <div><b>Remarks : </b>"+value[3]+"</div>\
                    ");

                    var inpData = {
                        ID:value[1]
                    };
                    // Fetch Prescription details
                    $.ajax({
                        url: 'getMedicineDetailsByEPrescriptionID',
                        type: 'GET',
                        dataType: 'json',
                        data: inpData,
                    })
                    .done(function(data) {
                        console.log("Order data:",data);
                        $("#medRespModalBody").append("\
                            <div><b> Issued for Prescription : </b>"+value[1]+"</div>\
                            <div style='margin-left:20px'><b>Symptoms:                  </b>"+data[0][0]+" </div>\
                            <div style='margin-left:20px'><b>Medicines Suggested:       </b>"+data[0][1]+" </div>\
                        ");

                    })
                    .fail(function(err) {
                        console.log("error");
                        console.log(err);
                    })
                    .always(function() {
                        console.log("complete");
                    });
                });
            });
        });
    })();
    

    // START: Popup defaults.

    // START: DON'T MODIFY following line required as per jquery.popup library.
    $.fn.popup.defaults.pagecontainer = '.popupClass';
    // END: DON'T MODIFY following line required as per jquery.popup library.

    // START: Add the following divs to popup functionality.
    $('#basic').popup();        // For Request LabTest button
    $('#basic2').popup();       // For Book Medicines button 
    $('#basic3').popup();       // For Book Doctor Appointment button
    // END: Add the following divs to popup functionality.

    // Monkey patch CSS values since Bootstrap 4.0 is acting weird with buttons
    // having popup functionality.
    var topRowBtnHeight = $("#mainButtons").css("height");
    $("#reqLabTestBtn").css("height",topRowBtnHeight);
    $("#bookMedicineBtn").css("height",topRowBtnHeight);
    $("#bookApptBtn").css("height",topRowBtnHeight);

    // Fetch the patient's lab request documents on click of Request Lab Test 
    // button. Then show it in dropdown.
    $("#reqLabTestBtn").on("click",function(event) {
        $(".popupSearchTextBox").val("");
        $(".selectedSearchID").val("");
        $("#reqLabDocDropdown").empty();
        $.get('patientFetchLabDocs', function(data) {
            console.log(data);
            $.each(data, function(index, value) {
                $("#reqLabDocDropdown").append("\
                    <div class='labDoc dropdown-item' style='cursor:pointer'>"+
                        "<div class='testType'style='font-size:20px;'><b>Test Type:</b>"+value[4]+"</div>"+
                        "<div class='testDetails'style='font-size:15px;'>Details"+value[5]+"</div>"+
                        "<div class='labDocID' hidden>"+value[0]+"</div>"+
                    "</div>"
                );
                $(".labDoc").each(function (argument) {
                    $(this).on('click', function(event) {
                        // console.log($(this).children('.labDocID').text());
                        $("#selectedLabReqDocID").val($(this).children('.labDocID').text());
                        // console.log($(this).children('.testType').text());
                        $("#dropdownMenuLinkLabPopup").text($(this).children('.testType').text());
                        // console.log($("#selectedLabReqDocID").val());
                    });
                });
            });
        });
    });

    // Fetch the patient's unused prescriptions on click of Request Lab Test 
    // button. Then show it in dropdown.
    $("#bookMedicineBtn").on("click",function(event) {
        $(".popupSearchTextBox").val("");
        $(".selectedSearchID").val("");

        $("#reqPrescriptionDropdown").empty();
        $.get('patientFetchPrescriptions', function(data) {
            console.log(data);
            $.each(data, function(index, value) {
                $("#reqPrescriptionDropdown").append("\
                    <div class='prescriptionDoc dropdown-item' style='cursor:pointer'>"+
                        "<div class='prescriptionDocID:'style='font-size:20px;'><b>Prescription ID:</b>"+value[0]+"</div>"+
                        "<div class='prescriptionDetails'style='font-size:15px;'>Details"+value[2]+"</div>"+
                        "<div class='prescriptionDocID' hidden>"+value[0]+"</div>"+
                    "</div>"
                );
                $(".prescriptionDoc").each(function (argument) {
                    $(this).on('click', function(event) {
                        // console.log($(this).children('.labDocID').text());
                        $("#selectedPrescriptionID").val($(this).children('.prescriptionDocID').text());
                        // console.log($(this).children('.testType').text());
                        $("#dropdownMenuLinkPrescriptionPopup").text($(this).children('.prescriptionDocID').text());
                        // console.log($("#selectedLabReqDocID").val());
                    });
                });
            });
        });
    });

    // Booking appointments functionality was more complex and thus is on a
    // later stage.
    $("#bookApptBtn").on("click",function(event) {
        $(".popupSearchTextBox").val("");
        $(".selectedSearchID").val("");
    });

    // END : Popup defaults


    // START : Following lines are used to control the 
    // Set reminder functionalities in tabs.
    $("#doctorReminderOptions").show();
    $("#medicineReminderOptions").hide();
    $("#labTestReminderOptions").hide();

    $("#doctorReminder").on("click", function(argument) {
        $(".reminderSearchTextBox").attr("placeholder","Search for Doctors");
        $(".reminderSearchTextBox").attr("name","popupDoctorSearch");
        $(".setReminderBtn").attr("id","doctorSetReminderBtn");
        $("#doctorReminderMessage").show();
        $("#medicineReminderOptions").hide();
        $("#labTestReminderOptions").hide();
    });
    $("#medicineReminder").on("click", function(argument) {
        $(".reminderSearchTextBox").attr("placeholder","Search for Pharmacies");
        $(".reminderSearchTextBox").attr("name","popupMedicineSearch");
        $(".setReminderBtn").attr("id","medOrderSetReminderBtn");
        $("#doctorReminderMessage").hide();
        $("#medicineReminderOptions").show();
        $("#labTestReminderOptions").hide();
    });
    $("#labTestReminder").on("click", function(argument) {
        $(".reminderSearchTextBox").attr("placeholder","Search for Labs");
        $(".reminderSearchTextBox").attr("name","popupLabSearch");
        $(".setReminderBtn").attr("id","labTestSetReminderBtn");
        $("#doctorReminderMessage").hide();
        $("#labTestReminderOptions").show();
        $("#medicineReminderOptions").hide();
    });
    //END : Set Reminder tab functionalities.

    // START : Search functionality
    function getResTypeByName(name) {
        if(name.search("Doctor")!=-1)
        {
            return "Doctor";
        }
        else if(name.search("Medicine")!=-1)
        {
            // return "Medicine";
            return "Pharmacy";
        }
        else if(name.search("Lab")!=-1)
        {
            return "Lab";
        }
    }

    // All the search boxes in popups have same class .popupSearchTextBox .
    // Thus this single function handles search of all those search boxes.
    // Since the search is for LabDetails, DoctorDetails and PharmacyDetails 
    // tables in backend, this function fetches data if length is >=3, gets
    // type of data to be searched, makes AJAX call to commonSearch and then
    // displays the results in divs to appopriate place.
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
                    console.log(data);
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
                            $(".popupSearchResultsDiv").each(function(index,el){
                                $(this).on('click', function(event) {
                                    /* Act on the event */
                                    $("#popup"+inpData["resType"]+"Search").val($(this).text());
                                    $("#selected"+inpData["resType"]+"ID").val($(this).children(".popupSearchResultsID").text());
                                    $("#popup"+inpData["resType"]+"SearchResults").empty();
                                });
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
    // (Set) difference between two arrays.
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
    // Get appointment date. Based on date, get all times based on doctor's ID
    // in DoctorAppointment table, get difference to get available times and 
    // display the same
    $("#popupDoctorDate").on('blur', function(event) {
        $(".timeScroller").empty();
        var doctorID = $("#selectedDoctorID").val();
        var inpDate = getInputTypeDateByID("popupDoctorDate");
        setAvailableTimeSlots(doctorID,inpDate);
    });

    $("#doctorApptBookBtn").on('click',function(event) {
        event.preventDefault();
        /* Act on the event */
        var doctorID = $("#selectedDoctorID").val();
        var inpDate = getInputTypeDateByID("popupDoctorDate");
        
        // Get selected Doctor ID based on popupSearchTextBox's results.
        // Then send selected date and time to patientDoctorAppointment.
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
    // Similar functionality as Doctor Appointment booking button.
    $("#labBookBtn").on('click',function(event) {
        event.preventDefault();
        /* Act on the event */

        var payload = {
            labID : $("#selectedLabID").val(),
            apptDate : getTodayDate(),
            labRequestDocumentID : $("#selectedLabReqDocID").val()
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
    
    // Similar functionality as Doctor Appointment booking button.
    $("#medicineBookBtn").on('click',function(event) {
        event.preventDefault();
        /* Act on the event */

        var payload = {
            ePrescriptionID: $("#selectedPrescriptionID").val(),
            pharmacyID : $("#selectedPharmacyID").val(),
            pickupTime : getTodayDate(),

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
            $("#medicineBookMessage").append("\
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
            $("#medicineBookMessage").append("\
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

    // START: Set Doctor Reminder


    // END: Set Doctor Reminder

    /* End Adding your javascript here */
});