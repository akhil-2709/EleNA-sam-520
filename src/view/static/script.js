var selected = false;
var sourceFixed = false;
var destFixed = false;

var sourceCoordinates = "";
var destinationCoordinates = "";

var manualSourceAddress = "";
var manualDestinationAddress = "";

var limitingPercent = 0;

var shortestPathDist = 0;
var elenaPathDistance = 0;

function roundOff(N) {
    return Math.round(N*10000)/10000;
};

function setMapMarker(type, e) {
    if (type == "source") {
        document.getElementById("source").innerHTML = roundOff(e.lngLat["lat"])+","+roundOff(e.lngLat["lng"]);
        return new mapboxgl.Marker({color: "green"}).setLngLat(e.lngLat).addTo(map);
    } else {
        document.getElementById("destination").innerHTML = roundOff(e.lngLat["lat"])+","+roundOff(e.lngLat["lng"]);
        return new mapboxgl.Marker({color: "red"}).setLngLat(e.lngLat).addTo(map);
    }
}

function enableManualAddressFields(){
    const source = document.getElementById("source_manual");
    source.style.display = 'inline-block';

    const destination = document.getElementById("desti_manual");
    destination.style.display = 'inline-block';
};

function disableManualAddressFields(){
    const source = document.getElementById("source_manual");
    source.style.display = 'none';

    const destination = document.getElementById("desti_manual");
    destination.style.display = 'none';
};

function enableMapAddressFields(){
    const source = document.getElementById("source_map");
    source.style.display = 'inline-block';

    const destination = document.getElementById("desti_map");
    destination.style.display = 'inline-block';
};

function disableMapAddressFields(){
    const source = document.getElementById("source_map");
    source.style.display = 'none';

    const destination = document.getElementById("desti_map");
    destination.style.display = 'none';
};

function resetParameters() {
    selected = false;
    sourceFixed = false;
    destFixed = false;
    sourceCoordinates = "";
    destinationCoordinates = "";
    manualSourceAddress = "";
    manualDestinationAddress = "";
    limitingPercent = 0;

    marks = turf.featureCollection([]);
    map.getSource('circleData').setData(marks);

    if (sourceMarker) {
        sourceMarker.remove();
    }
    if (destMarker) {
        destMarker.remove();
    }
    document.getElementById("manualSourceAddress").value = "";
    document.getElementById("manualDestinationAddress").value = "";

    document.getElementById("limitingPercent").value = 0;

    document.getElementById("shortestPathDist").innerHTML = "";
    document.getElementById("shortestPathGain").innerHTML = "";

    document.getElementById("elenaPathDistance").innerHTML = "";
    document.getElementById("elenaPathGain").innerHTML = "";

    document.getElementById("source").innerHTML = "";
    document.getElementById("destination").innerHTML = "";

    disableManualAddressFields();
    disableMapAddressFields();

    resetOutputs();
}

function resetOutputs() {
    elenaPathDistance = 0;
    shortestPathDist = 0;

    if (map.getLayer("shortest_route")) {
        map.removeLayer("shortest_route")
    }
    if (map.getSource("shortest_route")) {
        map.removeSource("shortest_route")
    }
    if (map.getLayer("ele_route")) {
        map.removeLayer("ele_route")
    }
    if (map.getSource("ele_route")) {
        map.removeSource("ele_route")
    }
}

document.getElementById("manual").onclick = function(){
    disableMapAddressFields();
    enableManualAddressFields();
    selected = false;
};

document.getElementById("mapselect").onclick = function(){
    disableManualAddressFields();
    enableMapAddressFields();
    selected = true;
};

document.getElementById("reset").onclick = function(){
    resetParameters();
};

document.getElementById("submit").onclick = function(){
    var algo = $('input[name="algo"]:checked').val();
    var minimumMaximum = $('input[name="minimumMaximum"]:checked').val();

    limitingPercent = document.getElementById("limitingPercent").value;

    if (limitingPercent < 0) {
        alert("Percentage of the shortest path can't be negative. Please re-enter correct value for x before submitting.");
        return;
    }

    if (selected) {
        var submitData = {
            "source_coordinates": sourceCoordinates,
            "destination_coordinates": destinationCoordinates,
            "minimum_maximum": minimumMaximum.toString(),
            "algo": algo.toString(),
            "limiting_percent": limitingPercent
        }

        submitData = JSON.stringify(submitData);

        $.ajax({
            type: "POST",
            url: "/path_via_pointers",
            data: submitData,
            success: function(data) {
                plotRoute(data, "select")
                calcValues(data)
            },
            dataType: "json"
        });

    } else {
        manualSourceAddress = document.getElementById("manualSourceAddress").value.toString();
        manualDestinationAddress = document.getElementById("manualDestinationAddress").value.toString();

        if ((manualDestinationAddress.length==0) || (manualSourceAddress.length==0)) {
            window.alert("Enter valid Source and Destination Addresses!")
        }

        var submitData = {
            "manual_source_address": manualSourceAddress,
            "manual_destination_address": manualDestinationAddress,
            "minimum_maximum": minimumMaximum.toString(),
            "algo": algo.toString(),
            "limiting_percent": limitingPercent
        }

        submitData = JSON.stringify(submitData);

        $.ajax({
            type: "POST",
            url: "/path_via_address",
            data: submitData,
            success: function(data) {
                plotRoute(data, "address")
                calcValues(data)
            },
            dataType: "json"
        });
    }
};

function plotRoute(data, endpoint) {
    if(data["bool_pop"] == 0 || data["bool_pop"] == 1) {
        return;
    }

    if (data["bool_pop"] === -1) {
        if (sourceMarker) {
            sourceMarker.remove();
        }
        if (destMarker) {
            destMarker.remove();
        }
        resetOutputs();
        return;
    }

    map.addSource("ele_route", {
        "type": "geojson",
        "data": data["elev_path_route"]
    });

    map.addLayer({
        "id": "ele_route",
        "type": "line",
        "source": "ele_route",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "blue",
            "line-width": 5,
        }
    });

    map.addSource("shortest_route", {
        "type": "geojson",
        "data": data["shortest_route"]
    });

    map.addLayer({
        "id": "shortest_route",
        "type": "line",
        "source": "shortest_route",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "red",
            "line-width": 2
        }
    });

    calcValues(data);
}

function calcValues(data) {
    document.getElementById("shortestPathDist").innerHTML = data["shortDist"].toFixed(4) + " meters";
    document.getElementById("elenaPathDistance").innerHTML = data["elev_path_dist"].toFixed(4) + " meters";
    document.getElementById("shortestPathGain").innerHTML = data["gainShort"].toFixed(4) + " meters";
    document.getElementById("elenaPathGain").innerHTML = data["elev_path_gain"].toFixed(4) + " meters";
}

mapboxgl.accessToken = access_key;
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/navigation-night-v1',
    center: [-72.529262, 42.384803],
    zoom: 12,
});
var sourceMarker, destMarker;
marks = turf.featureCollection([]);

map.on("load" , function(){
    map.addSource('circleData', {
        type: 'geojson',
        data: {
        type: 'FeatureCollection',
        features: [],
        },
    });
    map.addLayer({
        id: 'data',
        type: 'circle',
        source: 'circleData',
        paint: {
        'circle-opacity' : 0.1,
        'circle-radius': 300,
        'circle-stroke-width': 2,
        'circle-stroke-color': '#333',
        },
    });
});

map.on('click', function(e){
    if(selected) {
        lngLat = new Array(e.lngLat.lng, e.lngLat.lat);
        if(!sourceFixed) {
            sourceMarker = setMapMarker('source', e);
            sourceCoordinates = JSON.stringify(e.lngLat);
            sourceFixed = true;
            map.flyTo({center: lngLat});
        } else if (!destFixed){
            destMarker = setMapMarker('destination', e);
            destinationCoordinates = JSON.stringify(e.lngLat);
            destFixed = true;
            map.flyTo({center: lngLat});
        }

    }
});
