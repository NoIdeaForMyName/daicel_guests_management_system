import { createTextTableField, filterRows, createHostsTableField } from './js/guests_service.js';

let guestsHistory;
let firstnameFilter;
let lastnameFilter;
let companyFilter;
let carFilter;
let dateStartFilter;
let dateEndFilter;
let timeStartFilter;
let timeEndFilter;
let historyTableBody;
let historyTable;
let noDataInfo;

document.addEventListener("DOMContentLoaded", () => {
    guestsHistory = JSON.parse(document.getElementById('guests_history_json').textContent);
    guestsHistory.forEach(arrival => {
        arrival.arrival_timestamp = new Date(arrival.arrival_timestamp);
        arrival.leave_timestamp = new Date(arrival.leave_timestamp);
    });

    // Initialize all filters
    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");
    carFilter = document.getElementById("car-filter");
    dateStartFilter = document.getElementById("date-start-filter");
    dateEndFilter = document.getElementById("date-end-filter");
    timeStartFilter = document.getElementById("time-start-filter");
    timeEndFilter = document.getElementById("time-end-filter");
    historyTableBody = document.getElementById("history-table-body");
    historyTable = document.getElementById("history");
    noDataInfo = document.getElementById("no-data-info");

    // Add event listeners to all filters
    [
        firstnameFilter, lastnameFilter, companyFilter, carFilter,
        dateStartFilter, dateEndFilter, timeStartFilter, timeEndFilter
    ].forEach(filter => {
        filter.addEventListener("input", () => filterAndDisplayHistory());
    });

    filterAndDisplayHistory();
});

function displayHistory(history) {
    historyTableBody.innerHTML = '';

    historyTable.style.display = history.length ? "block" : "none";
    noDataInfo.style.display = history.length ? "none" : "block";

    history.forEach(entry => {
        const row = document.createElement("tr");

        row.appendChild(createTextTableField(entry.name));
        row.appendChild(createTextTableField(entry.company));
        row.appendChild(createTextTableField(entry.register_number));
        row.appendChild(createTextTableField(entry.arrival_timestamp.toLocaleString()));
        row.appendChild(createTextTableField(entry.leave_timestamp.toLocaleString()));
        row.appendChild(createTextTableField(entry.description));

        const hostsCell = document.createElement("td");
        const badgeContainer = document.createElement("div");
        badgeContainer.className = "d-flex flex-wrap gap-2 align-items-center";

        row.appendChild(createHostsTableField(entry.hosts));

        historyTableBody.appendChild(row);
    });
}

function filterAndDisplayHistory() {
    const filtered = filterRows(
        guestsHistory,
        [
            firstnameFilter.value,
            lastnameFilter.value,
            companyFilter.value,
            carFilter.value,
            dateStartFilter.value,
            dateEndFilter.value,
            timeStartFilter.value,
            timeEndFilter.value
        ],
        [
            'firstname',
            'lastname',
            'company',
            'register_number',
            'date_start',
            'date_end',
            'time_start',
            'time_end'
        ]
    );
    displayHistory(filtered);
}