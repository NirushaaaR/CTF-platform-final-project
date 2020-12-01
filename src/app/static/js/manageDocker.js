const BASEURL = "http://139.162.48.22:3000/docker/";

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

// deploy docker button
const deployButton = document.createElement("input");
deployButton.classList.add("deploy-button")
deployButton.type = "button";
deployButton.value = "Deploy";

// delete docker button
const deleteButton = document.createElement("input");
deleteButton.classList.add("delete-button")
deleteButton.type = "button";
deleteButton.value = "Delete";

async function deleteDocker(docker) {
    try {
        const url = BASEURL + urlencode(docker);
        const res = await fetch(url, { method: "DELETE" });
        return await res.json();
    } catch (error) {
        return error;
    }
}

function checkDockerStatus(data, docker, isDelete, isDeleteLink) {
    const url = BASEURL + urlencode(docker);
    if (isDelete) {
        changeDeleteStatus(data);
    } else {
        changeDeployStatus(data);
    }

    setTimeout(function () {
        fetch(url)
            .then(res => res.json())
            .then(res => {
                const data = res.data;
                if (data.status === "deployed" && !isDelete) {
                    // deploy success!!
                    document.getElementById("id_url").disabled = false;
                    document.getElementById("id_url").value = res.url;
                    // submit form
                    document.getElementById("dockerweb_form").submit();
                } else if (data.status === "remove from server" && isDelete) {
                    // remove success
                    if (isDeleteLink) {
                        const deleteLink = document.querySelector(".deletelink").getAttribute("href");
                        window.location.replace(deleteLink);
                    } else {
                        console.table(data);
                        document.getElementById("id_url").disabled = false;
                        document.getElementById("id_url").value = "";
                        document.getElementById("dockerweb_form").submit();
                    }
                }
                else {
                    // check every 1.5 secconds
                    if (!data.isError) {
                        checkDockerStatus(data.status, docker, isDelete, isDeleteLink);
                    } else {
                        throw new Error(data.status);
                    }
                }
            })
            .catch(err => {
                document.querySelector(".deletelink").disabled = false;
                deployButton.disabled = false;
                deleteButton.disabled = false;
                changeDeployStatus(err);
            });
    }, 1500);
}

deployButton.addEventListener("click", function (e) {
    // e.preventDefault();
    deployButton.disabled = true;
    deleteButton.disabled = true;
    const docker = document.getElementById("id_docker").value;
    const port = document.getElementById("id_port").value;

    fetch(BASEURL, {
        // fetch("https://jsonplaceholder.typicode.com/posts", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ docker, port })
    })
        .then(res => res.json())
        .then(res => checkDockerStatus(res.status, docker, false, false))
        .catch(err => {
            deployButton.disabled = false;
            changeDeployStatus(err);
        });

    changeDeployStatus("uploading...");
});

deleteButton.addEventListener("click", function (e) {
    deployButton.disabled = true;
    deleteButton.disabled = true;

    const docker = document.getElementById("id_docker").value;
    fetch(BASEURL + urlencode(docker), {
        method: "DELETE",
    })
        .then(res => res.json())
        .then(res => checkDockerStatus(res.status, docker, true, false))
        .catch(err => {
            deployButton.disabled = false;
            deleteButton.disabled = true;
            changeDeleteStatus(err);
        });

    changeDeleteStatus("deleteing...");
});

const spanForDeploy = document.createElement("span");
spanForDeploy.id = "deploy-status";
spanForDeploy.setAttribute("style", "margin-left:3px");

function changeDeployStatus(text) {
    spanForDeploy.innerHTML = text;
}

const spanForDelete = document.createElement("span");
spanForDelete.id = "Delete-status";
spanForDelete.setAttribute("style", "margin-left:3px");

function changeDeleteStatus(text) {
    spanForDelete.innerHTML = text;
}

// div of all button
const divDeployButton = document.createElement("div");
divDeployButton.classList.add("form-row");
// add all button to div
divDeployButton.appendChild(deployButton);
divDeployButton.appendChild(spanForDeploy);

const divDeleteButton = document.createElement("div");
divDeleteButton.classList.add("form-row");
divDeleteButton.appendChild(deleteButton);
divDeleteButton.appendChild(spanForDelete);


document.addEventListener("DOMContentLoaded", function (e) {
    const formFieldset = document.querySelector("form fieldset");
    if (formFieldset !== null) {
        formFieldset.appendChild(divDeployButton);
        formFieldset.appendChild(divDeleteButton);
        document.getElementById("id_url").disabled = true;

        // delete link
        const deleteLinkButton = document.querySelector(".deletelink");
        if (deleteLinkButton != null) {
            deleteLinkButton.addEventListener("click", async function (e) {
                e.preventDefault();
                deleteLinkButton.disabled = true;
                const docker = document.getElementById("id_docker").value;
                const data = await deleteDocker(docker);
                checkDockerStatus(data.status, docker, true, true);
            });
        }

    }

}) 