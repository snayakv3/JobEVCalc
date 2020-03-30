const FAQ = document.querySelector(".faq-element")
const SAMPLEANCHOR = FAQ.querySelectorAll("a")[1]


function loadSampleData(e){
    e.preventDefault();
    var client = new XMLHttpRequest();
    client.open('GET', sampleTeamFile);
    client.onreadystatechange = function() {
        TEXTFORM.value = client.responseText;
    }
    client.send();
    enableCalcButton();
}

SAMPLEANCHOR.onclick = loadSampleData;
