const TEXTFORM = PAGE.querySelector(".calculate");
const CALCBUTTON = PAGE.querySelector("#button input");

var disabled = true;

function enableCalcButton(){
    CALCBUTTON.onclick = null;
    CALCBUTTON.classList.replace("disabled", "active");
    disabled = false;
}

function disableCalcButton(){
    CALCBUTTON.onclick = function(e){e.preventDefault()};
    CALCBUTTON.classList.replace("active", "disabled");
    disabled = true;
}

function updateCalcButton(){
    if(TEXTFORM.textLength > 0 && disabled){
        enableCalcButton();
    } else if (TEXTFORM.textLength == 0){
        disableCalcButton();
    }
}

updateCalcButton();
TEXTFORM.addEventListener("input", updateCalcButton);
