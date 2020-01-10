$(document).ready(function() { 
  
  $("#buttonPredict").click(function() { 
     
     $.ajax({
     	type: "GET",
	url: "/predict",
	success: function(response) {
	    $("#prediction").text(response.prediction);
            $.ajax({
		    type: "GET",
		    url: "/getImage",
		success: function(response){
			$("#foodImage").attr("src", response+"?"+(Date.now()));
		}
	    });
	}
     });
  }); 
});
