import { createTextTableField, filterRows } from './js/guests_service.js';

let activeGuests;
let firstnameFilter;
let lastnameFilter;
let companyFilter;
let carFilter;
let guestsTableBody;
let guestsTable;
let noDataInfo;

document.addEventListener("DOMContentLoaded", () => {
    activeGuests = JSON.parse(document.getElementById('active_guests_json').textContent);
    activeGuests.forEach(arrival => {
        arrival.arrival_timestamp = new Date(arrival.arrival_timestamp);
    });

    // Initialize filters and elements
    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");
    carFilter = document.getElementById("car-filter");
    guestsTableBody = document.getElementById("guests-table-body");
    guestsTable = document.getElementById("guests");
    noDataInfo = document.getElementById("no-data-info");

    // Add event listeners
    [firstnameFilter, lastnameFilter, companyFilter, carFilter].forEach(filter => {
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
        row.appendChild(createTextTableField(guest.register_number));
        row.appendChild(createTextTableField(guest.arrival_timestamp.toLocaleString()));
        row.appendChild(createTextTableField(guest.description));

        const hostsCell = document.createElement("td");
        guest.hosts.forEach(host => {
            hostsCell.innerHTML += `<p>${host.name}</p>`;
        });
        row.appendChild(hostsCell);

        guestsTableBody.appendChild(row);
    });
}

function filterAndDisplayGuests() {
    const filtered = filterRows(
        activeGuests,
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
    displayGuests(filtered);
}