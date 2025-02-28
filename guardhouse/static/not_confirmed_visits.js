import { createTextTableField, filterRows } from './guests_service.js';

let notConfirmedArrivals;

let firstnameFilter;
let lastnameFilter;
let companyFilter;

let arrivalsTableBody;

let arrivalsTable;
let noDataInfo;

const CONFIRM_VISIT_URL = "confirm-visit/";

document.addEventListener("DOMContentLoaded", (event) => {
    notConfirmedArrivals = JSON.parse(document.getElementById('not_confirmed_arrivals_json').textContent);

    arrivalsTableBody = document.getElementById("arrivals-table-body");

    // implement filtering on change event listener ...
    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");

    arrivalsTable = document.getElementById("arrivals");
    noDataInfo = document.getElementById("no-data-info");

    firstnameFilter.addEventListener("input", () => filterAndDisplayRows());
    lastnameFilter.addEventListener("input", () => filterAndDisplayRows());
    companyFilter.addEventListener("input", () => filterAndDisplayRows());

    //displayArrivals(notConfirmedArrivals);
    filterAndDisplayRows();
});

function displayArrivals(arrivals) {
    arrivalsTableBody.innerHTML = '';

    arrivalsTable.style = arrivals.length > 0 ? "display:block" : "display:none;"
    noDataInfo.style = arrivals.length < 1 ? "display:block" : "display:none;"

    for (let arrival of arrivals) {
        let row = document.createElement("tr");

        row.appendChild(createTextTableField(arrival.name));
        row.appendChild(createTextTableField(arrival.company));
        row.appendChild(createTextTableField(arrival.description));

        let hostsTableNode = document.createElement("td");
        for (let host of arrival.hosts) {
            hostsTableNode.innerHTML += `<p>${host.name}</p>`;
        }
        row.appendChild(hostsTableNode);

        row.appendChild(createUrlTableField(arrival.id));

        arrivalsTableBody.appendChild(row);
    }
}

function createUrlTableField(id) {
    let actionTableNode = document.createElement("td");
    let actionNode = document.createElement("a");
    actionNode.href = CONFIRM_VISIT_URL + String(id);
    actionNode.textContent = "Potwierdź wizytę";
    actionTableNode.appendChild(actionNode);
    return actionTableNode;
}

function filterAndDisplayRows() {
    let filtered = filterRows(
        notConfirmedArrivals,
        [
            firstnameFilter.value,
            lastnameFilter.value,
            companyFilter.value,
        ],
        [
            'firstname',
            'lastname',
            'company',
        ]
    );
    displayArrivals(filtered);
}
