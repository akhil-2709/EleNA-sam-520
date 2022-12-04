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

function setMapMarker(type, e) {
    if (type == "source") {
        document.getElementById("source").innerHTML = e.lngLat["lat"]+","+e.lngLat["lng"];
        return new mapboxgl.Marker({color: "blue"}).setLngLat(e.lngLat).addTo(map);
    } else {
        document.getElementById("destination").innerHTML = e.lngLat["lat"]+","+e.lngLat["lng"];
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
        alert("Wrong Percentage!!!");
        return;
    }

    if (selected) {
        var submitData = {
            "source_coordinates": sourceCoordinates,
            "destination_coordinates": destinationCoordinates,
            "minimum_maximum": minimumMaximum,
            "algo": algo,
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
            window.alert("Problem!!!!!!")
        }

        var submitData = {
            "manual_source_address": manualSourceAddress,
            "manual_destination_address": manualDestinationAddress,
            "minimum_maximum": minimumMaximum,
            "algo": algo,
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
