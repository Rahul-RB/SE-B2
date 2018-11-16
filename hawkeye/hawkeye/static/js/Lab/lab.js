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
     
     $("#search_bar1").on("keyup", function() {
        var value = $(this).val();
        var search_p = $("#search_param1").val();
        //console.log(search_p);
        $("#myTable1").filterTable(value, search_p);
       
    });
    $("#search_bar2").on("keyup", function() {
        var value = $(this).val();
        var search_p = $("#search_param2").val();
        //console.log(search_p);
        $("#myTable2").filterTable(value, search_p);
       
    }); 
        
    (function($) {
        $.fn.filterTable = function(filter, columnname) {
            var index = null;
            this.find("thead > tr:first > th").each(function(i) {
                if ($.trim($(this).text()) == columnname) {
                    index = i;
                    return false;
                }
            });
            if (index == null)
                throw ("filter columnname: " + columnname + " not found");
            this.find("tbody:first > tr").each(function() {
                var row = $(this);
                if (filter == "") {
                    row.show();
                }
                else {
                    var cellText = row.find("td:eq(" + index + ")").find('option:selected').text();
                    if (cellText == "") {
                        cellText = $(row.find(("td:eq(" + index + ")"))).text();
                    }
                    if (cellText.indexOf(filter) == -1) {
                        row.hide();
                    }
                    else {
                        row.show();
                    }
                }
            });
            return this;
        };

    })(jQuery);
    /* End Adding your javascript here */
	
   	/*function appendTableColumn(table, rowData) {
  		var lastRow = $('<tr/>').appendTo(table.find('tbody:last'));
 	 	$.each(rowData, function(colIndex, c) { 
      			lastRow.append($('<td/>').text(c));
  		});
   
  		return lastRow;
		}
 
	$(document).ready(function() {
   	 var table = makeTable(data);
    	appendTableColumn(table, ["Calgary", "Ottawa", "Yellowknife"]);
	});*/
});
        
