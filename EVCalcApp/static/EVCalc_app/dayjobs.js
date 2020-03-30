const DAYELEMENT = PAGE.querySelector(".day-element");
const JOBINFO = DAYELEMENT.querySelectorAll(".job-info-element");
const DAYCHECKS = DAYELEMENT.querySelectorAll(".day-num-check input")
const DAYTEXT = DAYELEMENT.querySelectorAll(".day-num-check a");
const ALLANCHOR = DAYELEMENT.querySelector(".day-title a");
const ALLANCHORTEXT = ["show all", "hide all"];

var displayed = false;
var jobShown = -1;

function toggleInfo(num){
    if(jobShown != -1){
        PAGE.querySelector(".job-element").remove();
        DAYTEXT[jobShown].style.color="grey";
    }

    if(num != -1 && jobShown != num){
        copiedJob = JOBINFO[num].cloneNode(true);
        copiedJob.removeAttribute("hidden");
        dayTitle = document.createElement("h2");
        dayTitle.innerHTML = "Day " + (num+1);

        if(DAYCHECKS[num].checked){
            dayTitle.style.textDecoration = "line-through";
            dayTitle.style.color = "red";
        }

        newJobElement = document.createElement("div");
        newJobElement.classList.add("job-element");
        newJobElement.appendChild(dayTitle);
        newJobElement.appendChild(copiedJob);
        PAGE.appendChild(newJobElement);
        DAYTEXT[num].style.color="black";
    }

    editHeader();
    jobShown = jobShown == num ? -1 : num;
}

function toggleAllInfo(e){
    e.preventDefault();
    for(let i=0; i < DAYTEXT.length; i++){
        if(!displayed && JOBINFO[i].hasAttribute("hidden")){
            JOBINFO[i].removeAttribute("hidden");
        } else if(displayed){
            JOBINFO[i].setAttribute("hidden", true);
        }
    }

    displayed = !displayed;
    ALLANCHOR.innerHTML="[" + ALLANCHORTEXT[displayed+0] +"]";
    editHeader();
}

function reveal(e, num){
    e.preventDefault();
    toggleInfo(num);
}

function changeDayTitle(num){
    if(jobShown == num){
        dayTitle = PAGE.querySelector(".job-element h2");
        if(DAYCHECKS[num].checked){
            dayTitle.style.textDecoration = "line-through";
            dayTitle.style.color = "red";
        } else{
            dayTitle.style.textDecoration = null;
            dayTitle.style.color = null;
        }
    }
}

for(let i=0; i < DAYTEXT.length; i++){
    DAYTEXT[i].onclick = function(e){reveal(e,i)};
    DAYCHECKS[i].onclick = function(e){changeDayTitle(i)};
}

ALLANCHOR.onclick = toggleAllInfo;
