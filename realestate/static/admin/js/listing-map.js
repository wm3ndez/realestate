function initializeMap() {
    var coords_field = document.getElementById('id_coords');
    var coords = coords_field.value.split(',');
    var myLatlng = new google.maps.LatLng(coords[0], coords[1]);
    var mapOptions = {
        zoom: 8,
        center: myLatlng
    }
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        animation: google.maps.Animation.DROP,
        draggable: true
    });

    google.maps.event.addListener(marker, 'dragend', function () {
        var position = marker.getPosition();
        coords_field.value = position.lat() + ',' + position.lng();
    });
}

google.maps.event.addDomListener(window, 'load', initializeMap);