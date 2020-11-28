const BASEURL = "http://workspace:3000/docker/";

function urlencode(str) {
    return encodeURIComponent(str)
        .replace(/!/g, '%21')
        .replace(/'/g, '%27')
        .replace(/\(/g, '%28')
        .replace(/\)/g, '%29')
        .replace(/\*/g, '%2A')
        .replace(/~/g, '%7E')
        .replace(/%20/g, '+')
}

async function deleteDocker(docker) {
    try {
        const url = BASEURL + urlencode(docker);
        const res = await fetch(url, { method: "DELETE" });
        return await res.json();
    } catch (error) {
        return error;
    }
}

function checkDockerStatus(data, docker) {
    const url = BASEURL + urlencode(docker);
    console.log(data);

    setTimeout(function () {
        fetch(url)
            .then(res => res.json())
            .then(data => {
                changeDeployStatus("deploying...");
                console.log("status", data);
            })
            .catch(changeDeployStatus("error checking status:", err));
    }, 1000);
}

// div of all button
const divButton = document.createElement("div");
divButton.classList.add("form-row");

// deploy docker button
const deployButton = document.createElement("input");
deployButton.classList.add("deploy-button")
deployButton.type = "button";
deployButton.value = "Deploy";

deployButton.addEventListener("click", function (e) {
    // e.preventDefault();
    const docker = document.getElementById("id_docker").value;
    const port = document.getElementById("id_port").value;
    console.log(docker, port);

    fetch("http://workspace:3000/docker", {
        // fetch("https://jsonplaceholder.typicode.com/posts", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ docker, port })
    })
        .then(res => res.json())
        .then(res => checkDockerStatus(res, docker))
        .catch(err => changeDeployStatus(err));

    changeDeployStatus("uploading...");
    console.log("deploying check status every .. second");
})

const spanForDeploy = document.createElement("span");
spanForDeploy.id = "deploy-status";
spanForDeploy.setAttribute("style", "margin-left:3px");

function changeDeployStatus(text) {
    spanForDeploy.innerHTML = text;
}

// add all button to div
divButton.appendChild(deployButton);
divButton.appendChild(spanForDeploy);


document.addEventListener("DOMContentLoaded", function (e) {
    const formFieldset = document.querySelector("form fieldset");
    formFieldset.appendChild(divButton);
    document.querySelector(".field-is_deployed").hidden = true;
    // set checkbox by document.getElementById("id_is_deployed").checked = false
}) 