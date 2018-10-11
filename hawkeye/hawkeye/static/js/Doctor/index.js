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



    $(".addCF").click(function(){
        $("#customFields").append('<tr valign="top"><th scope="row"><label for="customFieldName">Symptoms and Medicines </label></th><td><input type="text" class="code" id="customFieldName" name="customFieldName[]" value="" placeholder="Enter symptoms here...." /> &nbsp; <input type="text" class="code" id="customFieldValue" name="customFieldValue[]" value="" placeholder="Enter medicines here...." /> &nbsp; <a href="javascript:void(0);" class="remCF">Remove</a></td></tr>');
    });

    $("#customFields").on('click','.remCF',function(){
        $(this).parent().parent().remove();
    });


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
