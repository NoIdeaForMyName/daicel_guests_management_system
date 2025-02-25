
let activeArrivals;
let filteredArrivals;

let firstnameFilter;
let lastnameFilter;
let companyFilter;
let carFilter;

let arrivalsTableBody;

document.addEventListener("DOMContentLoaded", (event) => {
    activeArrivals = JSON.parse(document.getElementById('active_arrivals_json').textContent);
    filteredArrivals = activeArrivals;

    arrivalsTableBody = document.getElementById("arrivals-table-body");

    // implement filtering on change event listener ...
    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");
    carFilter = document.getElementById("car-filter");

    firstnameFilter.addEventListener("input", () => filterRows());
    lastnameFilter.addEventListener("input", () => filterRows());
    companyFilter.addEventListener("input", () => filterRows());
    carFilter.addEventListener("input", () => filterRows());

    displayArrivals(activeArrivals);
});

function displayArrivals() {
    arrivalsTableBody.innerHTML = '';

    for (let arrival of filteredArrivals) {
        row = document.createElement("tr");

        row.appendChild(createTextTableField(arrival.name));
        row.appendChild(createTextTableField(arrival.company));
        row.appendChild(createTextTableField(arrival.register_number));
        row.appendChild(createTextTableField(arrival.arrival_timestamp));
        row.appendChild(createTextTableField(arrival.description));
        
        long_text_container = document.createElement("div");
        long_text_container.classList.add("long-text");
        for (let i=0; i < arrival.meetings.length; i++) {
            let meeting = arrival.meetings[i];
            let p = document.createElement("p");
            p.innerHTML = `<b>Spotkanie ${i+1}:</b> ${meeting.description}`;
            long_text_container.appendChild(p);
        }
        let meetingsTableNode = document.createElement("td");
        meetingsTableNode.appendChild(long_text_container);
        row.appendChild(meetingsTableNode);

        let hostsTableNode = document.createElement("td");
        for (let host of arrival.hosts) {
            hostsTableNode.innerHTML += `<p>${host.name}</p>`;
        }
        row.appendChild(hostsTableNode);

        row.appendChild(createCheckboxTableField(arrival.id));

        arrivalsTableBody.appendChild(row);
    }
}

function createTextTableField(text, hidden=false) {
    let tableNode = document.createElement("td");
    tableNode.textContent = text;
    tableNode.hidden = hidden
    return tableNode;
}
//<input type="checkbox" id="vehicle1" name="vehicle1" value="Bike">
function createCheckboxTableField(id) {
    let actionTableNode = document.createElement("td");
    let actionNode = document.createElement("input");
    actionNode.type = "checkbox";
    actionNode.name = "end-visit[]";
    actionNode.value = id;
    //actionNode.onclick = function() {endVisit([parseInt(this.parentNode.parentNode.firstChild.textContent)])};
    actionTableNode.appendChild(actionNode);
    return actionTableNode;
}

// function endVisits() {
//     //let ids = document.getElementsByClassName("end-visit-checkbox").map(node => parseInt(node.value));
//     let checkboxElements = document.getElementsByClassName("end-visit-checkbox");
//     let ids = Array.prototype.map.call(checkboxElements, element => parseInt(element.value));
//     console.log("Following visits will be ended: ", ids);
// }

function filterRows() {
    filteredArrivals = []

    let values = [
        firstnameFilter.value,
        lastnameFilter.value,
        companyFilter.value,
        carFilter.value
    ];
    values = values.map(v => v.trim().toLowerCase());

    let columns = [
        'firstname',
        'lastname',
        'company',
        'register_number'
    ];

    for (let arrival of activeArrivals) {
        let fulfills = true;
        for (let i=0; i < values.length; i++) {
            let value = values[i];
            if (value === '') {
                continue;
            }
            let column = columns[i];
            let columnValue;
            if (column === 'firstname' || column === 'lastname') {
                columnValue = arrival['name'].split(' ')[column === 'firstname' ? 0 : 1];
            }
            else {
                columnValue = arrival[column];
            }
            if (!columnValue) {
                fulfills = false;
                break;
            }
            if (columnValue && !columnValue.toLowerCase().trim().includes(value)) {
                fulfills = false;
                break;
            }
        }
        if (fulfills) {
            filteredArrivals.push(arrival);
        }
    }

    displayArrivals();
}

function endVisitsConfirmationPopup() {
    let counter = 0;
    document.getElementsByName("end-visit[]").forEach(el => {
        if (el.checked) {
            counter++;
        }
    });

    if (counter === 0) {
        alert("Nie wybrano żadnej wizyty!");
        return false;
    }

    return confirm(`Czy na pewno chcesz zakończyć wybrane wizyty? Liczba wybranych wizyt: ${counter}`);
}
