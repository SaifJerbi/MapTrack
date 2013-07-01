$(document).ready(function () {
	$.getJSON("/json_get_latest_waypoint/", function(json){
		   alert("JSON Data: "+   json.waypoints[0].geo_pos);
		   $('#showdata').html("<p>geo_pos="+json.waypoints[0].geo_pos+"</p>");
           $('#showdata').append("<p>voiture="+json.waypoints[0].voiture+"</p>");
           $('#showdata').append("<p>position="+json.waypoints[0].position+"</p>");  
		 });
});