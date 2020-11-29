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

// div of all button
const divButton = document.createElement("div");
divButton.classList.add("form-row");

// deploy docker button
const deployButton = document.createElement("input");
deployButton.classList.add("deploy-button")
deployButton.type = "button";
deployButton.value = "Deploy";

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
    changeDeployStatus(JSON.stringify(data));

    setTimeout(function () {
        fetch(url)
            .then(res => res.json())
            .then(res => {
                const data = res.data;
                changeDeployStatus(data.status);
                console.log("status", data);

                if (data.status === "deployed") {
                    // deploy success!!
                    document.getElementById("id_url").disabled = false;
                    document.getElementById("id_url").value = res.url;
                    // submit form
                    document.getElementById("dockerweb_form").submit();
                } else if ( data.status === "remove from server" ) {
                    // remove success
                    const deleteLink =  document.querySelector(".deletelink").getAttribute("href");
                    window.location.replace(deleteLink);

                } else {
                    // check every 1.5 secconds
                    checkDockerStatus(data, docker);
                }
            })
            .catch(err => {
                document.querySelector(".deletelink").disabled = false;
                deployButton.disabled = false;
                changeDeployStatus("error checking status:", err)
            });
    }, 1500);
}

deployButton.addEventListener("click", function (e) {
    // e.preventDefault();
    deployButton.disabled = true;
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
        .then(res => checkDockerStatus(res.status, docker))
        .catch(err => {
            deployButton.disabled = false;
            changeDeployStatus(err);
        });

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
    if (formFieldset !== null) {
        formFieldset.appendChild(divButton);
        document.getElementById("id_url").disabled = true;

        // delete link
        const deleteLinkButton = document.querySelector(".deletelink");
        if (deleteLinkButton != null) {
            deleteLinkButton.addEventListener("click", async function (e) {
                e.preventDefault();
                deleteLinkButton.disabled = true;
                const docker = document.getElementById("id_docker").value;
                const data = await deleteDocker(docker);
                checkDockerStatus(data.status, docker);
            });
        }

    }

}) 