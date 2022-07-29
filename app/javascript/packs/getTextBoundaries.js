async function sendBoxes() {
   
    const request_payload = {
        data: wordBoxes.words,
        time: wordBoxes.time,
        FID: wordBoxes.FID,
        UID: wordBoxes.UID
    }
    console.log(request_payload)
    
    try {
        const resp = await fetch(
          'http://127.0.0.1:3333/elementBoxes',
          {
            method: 'POST',
            mode: 'cors',  // Required for customizing HTTP request headers
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json; charset=UTF-8',  // Required for ``cherrypy.tools.json_in`` to identify JSON payload and parse it automatically
            },
            body: JSON.stringify(request_payload),
          },
        )
        const json_resp = await resp.json()
        // if for some reason the server is up, but has not found the survey page (usually due to it not being visible), send the data again
        if(!(json_resp.payload)) {
            sendBoxes();
        } 
//        console.log(json_resp)  
      } catch (e) {
        console.warn('Exception: ' + e);
        sendBoxes();
      }
}



function getWordBoxes(parentElt) {
    // if the element isn't selected, or does not contain text, exit
    if (parentElt == undefined || parentElt.nodeName !== '#text') {
        return null;
    }
    // initialize the range
    var range = document.createRange();
    // split text on special characters
    var words = parentElt.textContent.split(/[, \.\)\(_\|{};]/g);
    // if there's no words, exit
    // otherwise, process the text
    if (words.length == 0) {
        return null;
    }
    // initialze local variables 
    var start = 0;
    var end = 0;
    var wordList = [];
    var j = 0;
    
    // loops through each word in the split text, getting bounding boxes and 
    // cleaning junk characters 
    for (var i = 0; i < words.length; i++) {
        var word = words[i];
        end = start + word.length;
        range.setStart(parentElt, start);
        range.setEnd(parentElt, end);
        // not getBoundingClientRect as word could wrap
        var rects = range.getClientRects();
        
        // cleans up the text before adding it to the list
        // leaving these there means you get words like \t\t\t\t\t\t\tfooBar, 
        // which isn't helpful
        word = word.replace(/[\n\t\r\\\{\}\(\)"']/g, "");
        // checks that there is still a word to add before 
        // adding to list in an array with the bounding box
        if (word.length > 0) { 
            rects = getBoundingClientRect(rects);
            wordList[j++] = [word, rects];
        }
        // sets the start of the next range to the character after the 
        // end of the current range
        start = end + 1;
    }
    // if, after processing all the text, there's nothing left, exit 
    if (wordList.length == 0) {
        return null;
    }
    // otherwise return the array 
    return wordList;
    
}


// Converts the DOMRectList (which should only have one DOMRect in it) 
// into a normal dictionary, so it can be used easier. 
function getBoundingClientRect(element) {
    var rect = element[0];
    for (var i = 0; i < element.length; i++){
        var heightDiff = window.screen.height - window.innerHeight;
        var widthDiff = window.screen.width - window.innerWidth;
        console.log(heightDiff, window.screen.height, window.innerHeight);
        return {
            top: rect.top + heightDiff,
            right: rect.right + widthDiff,
            bottom: rect.bottom + heightDiff,
            left: rect.left + widthDiff,
            width: rect.width,
            height: rect.height,
            x: rect.x + heightDiff,
            y: rect.y + widthDiff,
        };
    }
}


const elements = document.querySelectorAll('div,code');
console.log(elements)


// Gets the bounding boxes of every word in a div, returns an array with an array for each div [[[words],[from],[div1], [[words],[from],[div2]]]]
var unix = Math.round(+new Date()/1000);
var wordBoxes = {};
wordBoxes['time'] = unix;
wordBoxes['words'] = [];
var i = 0;
for (var element of elements) { 
    //gets the bounding boxes of each word in this element 
    var boxes = getWordBoxes(element.childNodes[0])
    // if there are bounding boxes, add them all to the main array at the next position 
    // I could just add the array of bounding boxes to the main array, but this eliminates nested arrays
    if (boxes) {
        for (var j = 0; j < boxes.length; j++) {
            var box = boxes[j]; 
            var nextBox;
            if (nextBox = boxes[j+1]) {
                if (box[0] == 'FID'){
                    wordBoxes['FID'] = nextBox[0];
                }
                else if (box[0] == 'UID'){
                    wordBoxes['UID'] = nextBox[0];
                }
            }
            
        }
        wordBoxes['words'][i++] = boxes
    }
    
}



console.log(wordBoxes);
//saveText(JSON.stringify(wordBoxes), "text.txt");
sendBoxes();
