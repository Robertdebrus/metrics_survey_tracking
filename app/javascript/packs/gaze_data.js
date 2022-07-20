


function getWordBoxes(parentElt) {
    // if the element isn't selected, or does not contain text, exit
    if (parentElt == undefined || parentElt.nodeName !== '#text') {
        return null;
    }
    // initialize the range
    var range = document.createRange();
    // split text on special characters
    var words = parentElt.textContent.split(/[, \.\)\(_]/g);
    // if there's no words, exit
    // otherwise, process the text
    if (words.length == 0) {
        return null;
    }
    var start = 0;
    var end = 0;
    var wordList = [];
    var j = 0;
    for (var i = 0; i < words.length; i++) {
        var word = words[i];
        end = start + word.length;
        range.setStart(parentElt, start);
        range.setEnd(parentElt, end);
        // not getBoundingClientRect as word could wrap
        var rects = range.getClientRects();
        
        word = word.replace(/[\n\t\r\\\{\}\(\)"']/g, "");
        if (word.length > 0) {
            wordList[j++] = [word, rects];
        }
        start = end + 1;
    }
    // if, after processing the text, there's nothing left, exit 
    if (wordList.length == 0) {
        return null;
    }
    // otherwise return the array 
    return wordList;
    
}


function printElementCoordinates(e) {
    var rect = element.getBoundingClientRect();   
    console.log(rect)
} 




const elements = document.querySelectorAll('div,code');
console.log(elements)

var wordBoxes = [];
var i = 0;
for (element of elements) { 
    //console.log(element)
    //printElementCoordinates(element)
    var box = getWordBoxes(element.childNodes[0])
    if (box) {
        wordBoxes[i++] = box
    }
    
}
console.log(wordBoxes);



