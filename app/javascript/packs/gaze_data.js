function getCoordinates() {
    // GET
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://localhost:8080", true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            gazeController(xhr.responseText)
        } else {
            console.error(xhr.statusText);
        }
    };
    xhr.onerror = function () {
        console.error(xhr.statusText);
    };
    xhr.send(null);
    
}


function gazeController(idata) {
    //console.log(idata)
    try {
    idata = JSON.parse(idata);
    
    

    leye = idata['left_gaze_point'];
    reye = idata['right_gaze_point'];
    
    lx = leye[0];
    ly = leye[1];
    rx = reye[0];
    ry = reye[1];
    
    
    // averages the point between the left and right eye, 
    // them multiplies the x coordinate by the screen width 
    // and the y coordinate by the screen's hight, since by 
    // default the values are a number between 0 and 1, 
    // where 0,0 is the upper left corner, and 1,1 is the bottom right
        
    x = ((lx + rx) / 2) * screen.width;
    y = ((ly + ry) / 2) * screen.height;
    
    //console.log(x, y);
    
    var lookingAt = document.elementFromPoint(x, y);
    
    if(lookingAt.tagName == "CODE") {
        getTextAtPoint(x, y);
    }
    
    } catch (error) {}
}


function getTextAtPoint(x, y) {
    let range;
    let textNode;
    let offset;

    
    if (document.caretRangeFromPoint) {
        range = document.caretRangeFromPoint(x, y);
        textNode = range.startContainer;
        offset = range.startOffset;
     
    } else if (document.caretPositionFromPoint) {
        range = document.caretPositionFromPoint(x, y);
        textNode = range.offsetNode;
        offset = range.offset;
    } else {
        console.log("[This browser supports neither"
          + " document.caretRangeFromPoint"
          + " nor document.caretPositionFromPoint.]");
        return;
    }
    //console.log(textNode);
    
    lookingAt = textNode.splitText(offset)
    
    if (textNode && textNode.nodeType == 3 && lookingAt.textContent != "") {
        console.log(lookingAt);
    }
    // Only split TEXT_NODEs
    /*
    if (textNode && textNode.nodeType == 3) {
    let replacement = textNode.splitText(offset);
    let br = document.createElement('br');
    textNode.parentNode.insertBefore(br, replacement);
    }
    */
}

let paragraphs = document.getElementsByTagName("p");
for (let i = 0; i < paragraphs.length; i++) {
  paragraphs[i].addEventListener('click', insertBreakAtPoint, false);
}


// Accepts an element, and highlights it for a time, after which it returns to its normal color
function highlight(element) {
    let defaultBG = element.style.backgroundColor;
    let defaultTransition = element.style.transition;

    if(defaultBG != "#FDFF47") {
        element.style.transition = "background 1s";
        element.style.backgroundColor = "#FDFF47";
        setTimeout(function()
        {
            element.style.backgroundColor = defaultBG;
            setTimeout(function() {
                element.style.transition = defaultTransition;
            }, 1000);
        }, 400);
    }
}


//  Repeating Function
setInterval(getCoordinates, 50);  

