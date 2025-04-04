import { createTextTableField, filterRows } from './guests_service.js';

let notConfirmedGuests;
let firstnameFilter;
let lastnameFilter;
let companyFilter;
let guestsTableBody;
let guestsTable;
let noDataInfo;

document.addEventListener("DOMContentLoaded", () => {
    notConfirmedGuests = JSON.parse(document.getElementById('not_confirmed_guests_json').textContent);

    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");
    guestsTableBody = document.getElementById("guests-table-body");
    guestsTable = document.getElementById("guests");
    noDataInfo = document.getElementById("no-data-info");

    // Event listeners for filters
    [firstnameFilter, lastnameFilter, companyFilter].forEach(filter => {
        filter.addEventListener("input", () => filterAndDisplayGuests());
    });

    filterAndDisplayGuests();
});

function displayGuests(guests) {
    guestsTableBody.innerHTML = '';

    guestsTable.style.display = guests.length ? "block" : "none";
    noDataInfo.style.display = guests.length ? "none" : "block";

    guests.forEach(guest => {
        const row = document.createElement("tr");

        row.appendChild(createTextTableField(guest.name));
        row.appendChild(createTextTableField(guest.company));
        row.appendChild(createTextTableField(guest.description));

        const hostsCell = document.createElement("td");
        guest.hosts.forEach(host => {
            hostsCell.innerHTML += `<p>${host.name}</p>`;
        });
        row.appendChild(hostsCell);

        const actionsCell = document.createElement("td");
        actionsCell.innerHTML = `<a href="/host/edit_guest/${guest.id}" class="edit-link">Edytuj</a>`;
        row.appendChild(actionsCell);

        guestsTableBody.appendChild(row);
    });
}

function filterAndDisplayGuests() {
    const filtered = filterRows(
        notConfirmedGuests,
        [
            firstnameFilter.value,
            lastnameFilter.value,
            companyFilter.value
        ],
        [
            'firstname',
            'lastname',
            'company'
        ]
    );
    displayGuests(filtered);
}