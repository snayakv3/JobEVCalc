const BODY = document.querySelector("body");
const HEADER = BODY.querySelector(".header");
const ERRORS = BODY.querySelector(".errors");
const PAGE = BODY.querySelector(".page");

var windowResize = false;
var errorInitialized = false;
function editHeader(){
    let windowWidth = window.innerWidth;
    width = PAGE.clientWidth > windowWidth ? PAGE.clientWidth : windowWidth;
    if(HEADER.clientWidth != width){
        HEADER.setAttribute("style","width:"+width+"px;");
        if(ERRORS != null){
            setErrors(width);
        }
    }

    if(ERRORS != null && !errorInitialized){
        HEADER.style.borderBottomColor = "red"
        setErrors(width);
    } else if(ERRORS == null && !errorInitialized){
        HEADER.style.borderBottomColor = "white"
    }
}

function closeErrors(e){
    e.preventDefault();
    let closeButton = ERRORS.querySelector(".close-button");
    BODY.removeChild(ERRORS);
    HEADER.style.borderBottomColor = "white";
}

function setErrors(width){
    let closeButton = ERRORS.querySelector(".close-button")
    ERRORS.setAttribute("style","width: "+width+"px")

    if(!errorInitialized){
        closeButton.onclick = closeErrors
        errorInitialized = true;
    }
}

editHeader();
window.addEventListener("resize", function(){
    windowResize = true;
    editHeader();
})
