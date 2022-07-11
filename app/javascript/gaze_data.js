
function getCoordinates() {
    // GET
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://localhost:8080", true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            //var jsonString = xhr.responseText;
            //var coordsDict = JSON.parse(jsonString);
            console.log(xhr.responseText)
        } else {
            console.error(xhr.statusText);
        }
    };
    xhr.onerror = function () {
        console.error(xhr.statusText);
    };
    xhr.send(null);
    
    // POST
    var xhr2 = new XMLHttpRequest();
    xhr2.open("POST", "http://localhost:8080", true);

    xhr2.onerror = function(e) {
        console.error(xhr.statusText);
    };

    var data = {"message": coordsDict};
    var jsondata = JSON.stringify(data);
    xhr2.send(jsondata);
    
    // Looking At
    //gazeDetector(xCoords, yCoords);
}

//  Repeating Function
setInterval(getCoordinates, 2000);  

