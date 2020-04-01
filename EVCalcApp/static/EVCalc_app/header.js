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
    else if(ERRORS != null){
        setErrors(width)
        HEADER.style.borderBottomColor = "red"
    }


    windowResize = false;
}

function closeErrors(){
    let closeButton = ERRORS.querySelector(".close-button")
    BODY.removeChild(ERRORS)
    HEADER.style.borderBottomColor = "white"
    closeButton.onclick = null
}

function setErrors(width){
    let closeButton = ERRORS.querySelector(".close-button")
    ERRORS.setAttribute("style","width: "+width+"px")

    if(closeButton.onclick == null){
        closeButton.onclick = closeErrors
    }
}

editHeader();
window.addEventListener("resize", function(){
    windowResize = true;
    editHeader();
})
