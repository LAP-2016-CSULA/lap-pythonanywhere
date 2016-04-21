var markers = {};
var map = {};
var trees = document.querySelectorAll('[class*="tree"]');
var CSULA_LONG = -118.169276, CSULA_LAT = 34.065975;


function initialize() {
    var mapProp = {
        center: new google.maps.LatLng(CSULA_LAT, CSULA_LONG),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
        
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    for (var i = 0; i < trees.length; i++) {
        var id = parseInt(trees[i].querySelectorAll('[class*="id"]')[0].textContent);
        var lat = parseFloat(trees[i].querySelectorAll('[class*="lat"]')[0].textContent);
        var long = parseFloat(trees[i].querySelectorAll('[class*="long"]')[0].textContent);
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, long),
        });
        marker.setMap(map);
        markers[String(id)] = marker;
    }
}
function on_marker_clicked(id) {
    if (String(id) in markers) {
        map.panTo(markers[String(id)].getPosition());
    }
}
// Add an Event Listener to Load the Map
google.maps.event.addDomListener(window, 'load', initialize);
