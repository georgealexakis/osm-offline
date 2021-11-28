// Add listeners on window
window.addEventListener('load', () => {
    // Map options
    var options =
    {
        selector: 'map',
        TILE_SRC: 'tiles-library/tiles/{z}/{x}/{y}.png',
        // Uncomment For World Imagery
        // TILE_SRC: 'tiles-library/tiles/{z}/{y}/{x}.png',
        currentZoom: 0,
        latLng: [35.31877, 25.10264],
        options: {
            minZoom: 0,
            maxZoom: 19
        }
    };
    var markers = [];
    var polyline = {};
    // Create a red polyline from an array of LatLng points
    var polylineCoordinates = [];

    // Init map with the options
    function initMap(options) {
        var map = L.map(options.selector).setView(options.latLng, options.currentZoom);

        // Tiles and marker
        L.tileLayer(options.TILE_SRC, options.options).addTo(map);
        addMarker({ latLng: options.latLng, message: 'Lat: ' + options.latLng[0] + ' Lng: ' + options.latLng[1] }, map);

        // Click event listener on marker
        map.on('click', (event) => {
            const coordinates = event.latlng;
            addPolyline(coordinates, map);
            addMarker({ latLng: [coordinates.lat, coordinates.lng], message: 'Lat: ' + coordinates.lat + ' Lng: ' + coordinates.lng }, map);
        });
    }
    // Add marker
    function addMarker(options, map) {
        var marker = L.marker(options.latLng, { draggable: true }).addTo(map)
            .bindPopup(options.message)
            .closePopup();

        // Add tooltip
        marker.bindTooltip('Lat: ' + options.latLng[0] + ' Lng: ' + options.latLng[1]).openTooltip();
        // Push to marker array
        markers.push(marker);
    }

    // Add polyline
    function addPolyline(coordinates, map) {
        polylineCoordinates.push([coordinates.lat, coordinates.lng]);
        polyline = L.polyline(polylineCoordinates, { color: 'red' }).addTo(map);
    }

    // Init map
    initMap(options);
});
