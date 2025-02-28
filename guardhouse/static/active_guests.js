import { createTextTableField, filterRows } from './guests_service.js';

let activeArrivals;

let firstnameFilter;
let lastnameFilter;
let companyFilter;
let carFilter;

let arrivalsTableBody;

let arrivalsTable;
let noDataInfo;

document.addEventListener("DOMContentLoaded", (event) => {
    activeArrivals = JSON.parse(document.getElementById('active_arrivals_json').textContent);

    arrivalsTableBody = document.getElementById("arrivals-table-body");

    // implement filtering on change event listener ...
    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");
    carFilter = document.getElementById("car-filter");

    arrivalsTable = document.getElementById("arrivals");
    noDataInfo = document.getElementById("no-data-info");

    firstnameFilter.addEventListener("input", () => filterAndDisplayRows());
    lastnameFilter.addEventListener("input", () => filterAndDisplayRows());
    companyFilter.addEventListener("input", () => filterAndDisplayRows());
    carFilter.addEventListener("input", () => filterAndDisplayRows());

    //displayArrivals(activeArrivals);
    filterAndDisplayRows();

    window.endVisitsConfirmationPopup = endVisitsConfirmationPopup;
});

function displayArrivals(arrivals) {
    arrivalsTableBody.innerHTML = '';

    arrivalsTable.style = arrivals.length > 0 ? "display:block" : "display:none;"
    noDataInfo.style = arrivals.length < 1 ? "display:block" : "display:none;"

    for (let arrival of arrivals) {
        let row = document.createElement("tr");

        row.appendChild(createTextTableField(arrival.name));
        row.appendChild(createTextTableField(arrival.company));
        row.appendChild(createTextTableField(arrival.register_number));
        row.appendChild(createTextTableField(arrival.arrival_timestamp));
        row.appendChild(createTextTableField(arrival.description));

        let hostsTableNode = document.createElement("td");
        for (let host of arrival.hosts) {
            hostsTableNode.innerHTML += `<p>${host.name}</p>`;
        }
        row.appendChild(hostsTableNode);

        row.appendChild(createCheckboxTableField(arrival.id));

        arrivalsTableBody.appendChild(row);
    }
}

function createCheckboxTableField(id) {
    let actionTableNode = document.createElement("td");
    let actionNode = document.createElement("input");
    actionNode.type = "checkbox";
    actionNode.name = "end-visit[]";
    actionNode.value = id;
    actionTableNode.appendChild(actionNode);
    return actionTableNode;
}

function filterAndDisplayRows() {
    let filtered = filterRows(
        activeArrivals, 
        [
            firstnameFilter.value,
            lastnameFilter.value,
            companyFilter.value,
            carFilter.value
        ],
        [
            'firstname',
            'lastname',
            'company',
            'register_number'
        ]
    );
    displayArrivals(filtered);
}

export function endVisitsConfirmationPopup() {
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
