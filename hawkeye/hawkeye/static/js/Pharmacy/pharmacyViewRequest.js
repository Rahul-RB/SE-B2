$(document).ready(function() {
    $.ajax({
            url: 'prescriptionRequest'
        })
        .done(function(data) {
            console.log('success');
            appendStr = "<thead class='thead-inverse'><tr><th>Prescription ID</th><th>Patient ID</th><th>Medicine</th><th>Action</th></tr></thead><tbody>";

            /*$.each(data,function(index,value){
            appendStr = appendStr + "<tr><td>"+i+"</td><td>"+value[1]+"</td><td>"+value[2]+"</td></tr>"
            i+=1
            })*/
            id = 1;
            for (i in data) {
                l = data[i].length;
                a = i.split(" ");
                appendStr = appendStr + '<tr><td rowspan="' + l + '">' + a[0] + '</td><td rowspan="' + l + '">' + a[1] + '</td><td>' + data[i][0] + '</td>' + '<td rowspan="' + l + '"' + '><button id="' + id + '" role="button" data-toggle="modal" data-target="#login-modal" onclick=updateInfo(this.id,this)>done</button></td></tr>';
                for (j = 1; j < l; j++) {
                    appendStr = appendStr + '<tr><td>' + data[i][j] + '</td></tr>';
                }
                id += 1;
            }
            appendStr = appendStr + "</tbody>";
            $("#TableDisplay").append(appendStr);
        })
        .fail(function() {
            console.log('failed');
        })
        .always(function() {
            console.log('always');
        })
        //$("#TableDisplay").append("<thead class='thead-inverse'><tr><th>SL#</th><th>Patient_ID</th><th>Medicine</th><th> Action </th></tr></thead>");
    $("#submit").on("click", function(event) {
        event.preventDefault();
        var inpData = {
            patientID: $("#patientID").val(),
            prescriptionID: $("#prescriptionID").val(),
            response: $("#response").val(),
        }
        var jsonPayload = JSON.stringify(inpData);
        console.log(jsonPayload);
        $.ajax({
                url: 'prescriptionResponseUpdate',
                type: 'POST',
                dataType: 'json',
                data: jsonPayload,
                contentType: "application/json; charset=UTF-8"
            })
            .done(function(data) {
                console.log('success');
                console.log(data);
                location.reload();
            })
            .fail(function() {
                console.log('fail');
            })
            .always(function() {
                console.log('always');
            })
    });

    $(function() {

        var $formLogin = $('#login-form');
        var $formLost = $('#lost-form');
        var $formRegister = $('#register-form');
        var $divForms = $('#div-forms');
        var $modalAnimateTime = 300;
        var $msgAnimateTime = 150;
        var $msgShowTime = 2000;

        $('#login_register_btn').click(function() {
            modalAnimate($formLogin, $formRegister)
        });
        $('#register_login_btn').click(function() {
            modalAnimate($formRegister, $formLogin);
        });
        $('#login_lost_btn').click(function() {
            modalAnimate($formLogin, $formLost);
        });
        $('#lost_login_btn').click(function() {
            modalAnimate($formLost, $formLogin);
        });
        $('#lost_register_btn').click(function() {
            modalAnimate($formLost, $formRegister);
        });
        $('#register_lost_btn').click(function() {
            modalAnimate($formRegister, $formLost);
        });

        function modalAnimate($oldForm, $newForm) {
            var $oldH = $oldForm.height();
            var $newH = $newForm.height();
            $divForms.css("height", $oldH);
            $oldForm.fadeToggle($modalAnimateTime, function() {
                $divForms.animate({
                    height: $newH
                }, $modalAnimateTime, function() {
                    $newForm.fadeToggle($modalAnimateTime);
                });
            });
        }

        function msgFade($msgId, $msgText) {
            $msgId.fadeOut($msgAnimateTime, function() {
                $(this).text($msgText).fadeIn($msgAnimateTime);
            });
        }

        function msgChange($divTag, $iconTag, $textTag, $divClass, $iconClass, $msgText) {
            var $msgOld = $divTag.text();
            msgFade($textTag, $msgText);
            $divTag.addClass($divClass);
            $iconTag.removeClass("glyphicon-chevron-right");
            $iconTag.addClass($iconClass + " " + $divClass);
            setTimeout(function() {
                msgFade($textTag, $msgOld);
                $divTag.removeClass($divClass);
                $iconTag.addClass("glyphicon-chevron-right");
                $iconTag.removeClass($iconClass + " " + $divClass);
            }, $msgShowTime);
        }
    });

    function updateInfo(id, btn) {
        i = parseInt(id);
        var a = document.getElementById("TableDisplay");
        document.getElementById("prescriptionID").value = a.rows[i].cells[0].innerHTML;
        document.getElementById("patientID").value = a.rows[i].cells[1].innerHTML;
        //alert(a.rows[i].cells[0].innerHTML);

    }    
});
