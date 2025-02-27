
let author_json;
let hosts_json;

let descriptionInput;
let dateInput;
let timeStartInput;
let timeEndInput;

let leaderInput;

const LEADER_REGEX = /(\p{L}+) (\p{L}+)/u;

document.addEventListener("DOMContentLoaded", function() {
    author_json = JSON.parse(document.getElementById('author_json').textContent);
    hosts_json = JSON.parse(document.getElementById('hosts_json').textContent);

    descriptionInput = document.getElementById("description");
    dateInput = document.getElementById("date");
    timeStartInput = document.getElementById("start-time");
    timeEndInput = document.getElementById("end-time");

    leaderInput = document.getElementById("hosts-list");
});

function combineDatetime(date_str, time_str) {
    return date_str + ' ' + time_str;
}

function getAllLeadersFromTable() {
    let leadersTableBody = document.getElementById("leader-table-body");
    let leaders = []
    for (let row of leadersTableBody.childNodes) {
        let leader = {
            'id': parseInt(row.childNodes[0].textContent),
            'firstname': row.childNodes[1].textContent,
            'lastname': row.childNodes[2].textContent
        };
        leaders.push(leader);
    }
    return leaders;
}

function postMeetingData() {
    let description = descriptionInput.value;
    let startTimestamp = combineDatetime(dateInput.value, timeStartInput.value);
    let endTimestamp = combineDatetime(dateInput.value, timeEndInput.value);
    let leaders = getAllLeadersFromTable();

    // VALIDATION
    if (description === '') {
        alert("Uzupełnij opis spotkania!");
        return;
    }

    if (dateInput.value === '') {
        alert("Uzupełnij datę spotkania!");
        return;
    }

    if (timeStartInput.value === '') {
        alert("Uzupełnij czas rozpoczęcia spotkania!");
        return;
    }

    if (timeEndInput.value === '') {
        alert("Uzupełnij czas zakończenia spotkania!");
        return;
    }

    if (leaders.length < 1) {
        alert("Spotkanie musi być prowadzone przez conajmniej jednego gospodarza!");
        return;
    }

    let data = {
        'description': description,
        'start_timestamp': startTimestamp,
        'end_timestamp': endTimestamp,
        'leaders': leaders
    };

    console.log("DATA:\n", data);
    console.log("JSON:\n", JSON.stringify(data));
    console.log("Success");

    if (confirm('Czy napewno chcesz dodać nowe spotkanie?')) {
        sendFormToServer(data)
            .then(response => {
                alert("Spotkanie utworzone pomyślnie!");
                clearForm();
                scrollTop();
            })
            .catch(error => alert(`Error: ${error.message}`))
    }
}

function sendFormToServer(json) {
        return fetch('/host/add-meeting-process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'sessionid': getCookie('sessionid')
            },
            body: JSON.stringify(json)
        })
        .then(response => {
            console.log(response);
            return response.json()
            .then(data => {
                if (!response.ok) {
                    throw new Error(JSON.stringify(data));
                }
                return data;
            });
        });
}

function clearForm() {
    descriptionInput.value = '';
    dateInput.value = '';
    timeStartInput.value = '';
    timeEndInput.value = '';
    document.getElementById("hosts-list").value = '';
    document.getElementById("leader-table-body").innerHTML = ''
}

function scrollTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function getHostId(firstname, lastname) {
    for (let host of hosts_json) {
        if (host.firstname === firstname && host.lastname === lastname) {
            return host.id;
        }
    }
    return -1;
}

function addLeader() {

    let match = (leaderInput.value).match(LEADER_REGEX);
    if (!match) {
        alert("Podano nieprawidłowe dane prowadzącego!");
        return;
    }

    let leaderFirstname = match[1];
    let leaderLastname = match[2];
    let leaderId = getHostId(leaderFirstname, leaderLastname);

    if (leaderId === -1) {
        alert("Wprowadzony prowadzący nie istnieje w systemie!");
        return;
    }

    const newLeaderRow = document.createElement("tr");

    newLeaderRow.appendChild(createTextTableField(leaderId, display='none'));
    newLeaderRow.appendChild(createTextTableField(leaderFirstname));
    newLeaderRow.appendChild(createTextTableField(leaderLastname));
    newLeaderRow.appendChild(createCheckboxTableField());

    let leaderTableBody = document.getElementById("leader-table-body");
    leaderTableBody.appendChild(newLeaderRow);

    leaderInput.value = "";
}

function createTextTableField(text, display='') {
    let tableNode = document.createElement("td");
    tableNode.textContent = text;
    tableNode.style.display = display;
    return tableNode;
}

function createCheckboxTableField() {
    let actionTableNode = document.createElement("td");
    let actionNode = document.createElement("button");
    actionNode.textContent = "-";
    actionNode.onclick = function() {this.parentNode.parentNode.remove();};
    actionTableNode.appendChild(actionNode);
    return actionTableNode;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
