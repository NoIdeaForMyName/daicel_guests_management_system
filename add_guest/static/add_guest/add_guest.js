
let process_url;

let author_json;
let confirmed_json;
let hosts_data_json;
let companies_data_json;
let registered_guests_data_json;

let companyNameInput;
let registerNumberInput;
let descriptionInput;
let guestTableInput;
let hostTableInput;

const MAX_REGISTER_NB_LEN = 8;

document.addEventListener("DOMContentLoaded", (event) => {

    process_url = JSON.parse(document.getElementById('process_url_json').textContent);

    author_json = JSON.parse(document.getElementById('author_json').textContent);
    confirmed_json = JSON.parse(document.getElementById('confirmed_json').textContent);
    hosts_data_json = JSON.parse(document.getElementById('hosts_data_json').textContent);
    companies_data_json = JSON.parse(document.getElementById('companies_data_json').textContent);
    registered_guests_data_json = JSON.parse(document.getElementById('registered_guests_data_json').textContent);

    companyNameInput = document.getElementById("companies-list");
    registerNumberInput = document.getElementById("register-nb");
    descriptionInput = document.getElementById("arrival-purpose");
    guestTableInput = document.getElementById("guest-table-body");
    hostTableInput = document.getElementById("host-table-body");

    companyNameInput.addEventListener("blur", () => {
        const companyName = companyNameInput.value;
        if (!validateCompany(companyName)) {
            alert("Wprowadzona nazwa firmy jest nieznana i zostanie dodana. Jeśli to błąd - zmień nazwę firmy")
        }

    });
    //
    // document.getElementById("add-guest").addEventListener('click', addGuest);
    // document.getElementById("add-host").addEventListener('click', addHost);
    // document.getElementById("submit-button").addEventListener('click', postGuestData);
});

function getDataFromTable(tableBody) {
    let values = [];
    for (let row of tableBody.children) {
        let value = []
        for (let el of Array.from(row.children).slice(0, -1)) {
            value.push(el.textContent);
        }
        values.push(value);
    }
    return values;
}

async function postGuestData() {
    let companyValue = companyNameInput.value;
    let registerNbValue = registerNumberInput.value;
    let descriptionValue = descriptionInput.value;
    let guestsValues = getDataFromTable(guestTableInput);
    let hostsValues = getDataFromTable(hostTableInput);

    if (!validateRegisterNb(registerNbValue)) {
        alert("Nieprawidłowy numer tablicy rejestracyjnej!");
        registerNumberInput.textContent = "";
        return;
    }

    if (descriptionValue.length === 0) {
        alert("Nie podano celu przybycia");
        return;
    }

    if (guestsValues.length === 0) {
        alert("Musisz wprowadzić dane przynajmniej jednego gościa!");
        return;
    }

    if (hostsValues.length === 0) {
        alert("Musisz wprowadzić dane przynajmniej jednego gospodarza!");
        return;
    }

    const confirmMsg = `Czy napewno chcesz dodać gościa?${confirmed_json ? `\nCzas przybycia: ${new Date()}` : ""}`
    if (confirm(confirmMsg)) {
        sendFormToServer({
            //'author': author_json,
            'confirmed': confirmed_json,
            'company': companyValue,
            'register_number': registerNbValue,
            'description': descriptionValue,
            'guests': guestsValues.map(guest => ({'id': Number(guest[0]), 'firstname': guest[1], 'lastname': guest[2]})),
            'hosts': hostsValues.map(host => ({'id': Number(host[0]), 'firstname': host[1], 'lastname': host[2]})),
        })
        .then(response => {
            clearForm();
            //location.reload();
            scrollTop();
        })
        .catch(error => {
            alert(`Error: ${error.message.slice(1, -1)}`);
        });
    }
}

function sendFormToServer(json) {
    console.log("FORM:", json);
    return fetch(process_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(json)
    })
    .then(response => {
        return response.json()
        .then(data => {
            if (!response.ok) {
                throw new Error(JSON.stringify(data.error));
            }
            return data;
        });
    });
}

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

function validateCompany(name) {
    return (companies_data_json.map(comp_data => comp_data.name)).includes(name);
}

function validateRegisterNb(registerNb) {
    return registerNb.length <= MAX_REGISTER_NB_LEN;
}

// function getAllFields() {
//     return {
//         "company": 
//     }
// }

function clearForm() {
    companyNameInput.value = '';
    registerNumberInput.value = '';
    descriptionInput.value = '';
    guestTableInput.innerHTML = ''
    hostTableInput.innerHTML = ''
}

function scrollTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function addHost() {
    const HOST_REGEX = /(\p{L}+) (\p{L}+)/u;
    let hostNode = document.getElementById("hosts-list");
    const host = hostNode.value;
    let match = host.match(HOST_REGEX);
    if (!match) {
        alert("Błędny format danych gospodarza")
        return;
    }

    //const id = parseInt(match[1]); // TIDI
    const fname = match[1];
    const lname = match[2];
    const id = registeredHostId(fname, lname);
    console.log(fname, lname, id);

    if (!(hosts_data_json.map(host => host.id)).includes(id)) {
        // wrong value!
        alert("Podano nieprawidłowe dane gospodarza");
        hostNode.textContent = "";
        return;
    }

//            const host_to_add = hosts_data_json.filter(host => host.id===id)[0];

    const newHostRow = document.createElement("tr");

    newHostRow.appendChild(createTextTableField(id, 'none'));
    newHostRow.appendChild(createTextTableField(fname));
    newHostRow.appendChild(createTextTableField(lname));    
    newHostRow.appendChild(createCheckboxTableField());

    let hostTableBody = document.getElementById("host-table-body");
    hostTableBody.appendChild(newHostRow);

    hostNode.value = "";
}

function addGuest() {
    let fnameNode = document.getElementById("guest-fname");
    const fname = fnameNode.value;
    let lnameNode = document.getElementById("guest-lname");
    const lname = lnameNode.value;
    console.log(fname);
    console.log(lname);
    if (!fname || !lname) {
    alert("Proszę wpisać imię i nazwisko.");
    return;
    }

    const newGuestRow = document.createElement("tr");

    const id = registeredGuestId(fname, lname);

    if (id === -1) {
        alert("Wprowadzony gość nie istnieje w systemie i zostanie utworzony. Jeśli to błąd - usuń gościa z listy");
    }

    newGuestRow.appendChild(createTextTableField(id, 'none'));
    newGuestRow.appendChild(createTextTableField(fname));
    newGuestRow.appendChild(createTextTableField(lname));
    newGuestRow.appendChild(createCheckboxTableField());

    let guestTableBody = document.getElementById("guest-table-body");
    guestTableBody.appendChild(newGuestRow);

    fnameNode.value = "";
    lnameNode.value = "";
}

function registeredGuestId(firstname, lastname) {
    for (let guest of registered_guests_data_json) {
        if (guest.firstname === firstname && guest.lastname === lastname) {
            return guest.id;
        }
    }
    return -1;
}

function registeredHostId(firstname, lastname) {
    for (let host of hosts_data_json) {
        if (host.firstname === firstname && host.lastname === lastname) {
            return host.id;
        }
    }
    return -1;
}

function createTextTableField(text, display='') {
    let tableNode = document.createElement("td");
    tableNode.textContent = text;
    tableNode.style.display = display;
    tableNode.className = "align-middle";
    return tableNode;
}

function createCheckboxTableField() {
    let actionTableNode = document.createElement("td");
    let actionNode = document.createElement("button");
    actionNode.className = "btn btn-danger btn-sm";
    actionNode.innerHTML = '<i class="bi bi-trash"></i>';
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
