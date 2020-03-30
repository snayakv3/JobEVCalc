const BODY = document.querySelector("body");
const HEADER = BODY.querySelector(".header");
const ERRORS = BODY.querySelector(".errors");
const PAGE = BODY.querySelector(".page");

var windowResize = false;
function editHeader(){
    let windowWidth = window.innerWidth;

    width = PAGE.clientWidth > windowWidth ? PAGE.clientWidth : windowWidth;
    if(HEADER.clientWidth != width){
        HEADER.setAttribute("style","width:"+width+"px;");
        if(ERRORS != null){
            setErrors(width);
        }
    }
    if(ERRORS != null){
        HEADER.style.borderBottomColor = "red"
    }


    windowResize = false;
}

function closeErrors(){
    BODY.removeChild(ERRORS)
    HEADER.style.borderBottomColor = "white"
}

function setErrors(width){
    let closeButton = ERRORS.querySelector(".close-button")
    ERRORS.setAttribute("style","width: "+width+"px")

    if(!windowResize){
        closeButton.onclick = closeErrors
    }
}

editHeader();
window.addEventListener("resize", function(){
    windowResize = true;
    editHeader();
})
