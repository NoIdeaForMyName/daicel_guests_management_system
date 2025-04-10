import {createCheckboxTableField, createTextTableField, filterRows} from './js/guests_service.js';

let notConfirmedArrivals;

let endFormPopup;
let showPopupButton;
let closePopupButton;

let firstnameFilter;
let lastnameFilter;
let companyFilter;

let arrivalsTableBody;

let arrivalsTable;
let noDataInfo;

document.addEventListener("DOMContentLoaded", (event) => {
    notConfirmedArrivals = JSON.parse(document.getElementById('not_confirmed_arrivals_json').textContent);

    const modal = new bootstrap.Modal(document.getElementById('endFormModal'));

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

    window.confirmVisitsConfirmationPopup = confirmVisitsConfirmationPopup;
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

        row.appendChild(createCheckboxTableField(arrival.id));

        arrivalsTableBody.appendChild(row);
    }
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

function confirmVisitsConfirmationPopup() {
    let counter = 0;
    document.getElementsByName("check[]").forEach(el => {
        if (el.checked) counter++;
    });

    if (counter === 0) {
        // Zamknij modal jeśli jest otwarty
        const modal = bootstrap.Modal.getInstance(document.getElementById('endFormModal'));
        if (modal) modal.hide();

        alert("Nie wybrano żadnej wizyty!");
        return false;
    }

    return confirm(`Czy na pewno chcesz potwierdzić ${counter} wybranych wizyt?`);
}
