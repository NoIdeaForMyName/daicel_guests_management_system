import { createTextTableField, filterRows } from './guests_service.js';

let historyArrivals;

let firstnameFilter;
let lastnameFilter;
let companyFilter;
let carFilter;
let arrivalDateStartFilter;
let arrivalDateEndFilter;
let arrivalTimeStartFilter;
let arrivalTimeEndFilter;

let arrivalsTableBody;

document.addEventListener("DOMContentLoaded", (event) => {
    historyArrivals = JSON.parse(document.getElementById('archive_arrivals_json').textContent);

    arrivalsTableBody = document.getElementById("arrivals-table-body");

    // implement filtering on change event listener ...
    firstnameFilter = document.getElementById("firstname-filter");
    lastnameFilter = document.getElementById("lastname-filter");
    companyFilter = document.getElementById("company-filter");
    carFilter = document.getElementById("car-filter");
    arrivalDateStartFilter = document.getElementById("arrival-date-start-filter");
    arrivalDateEndFilter = document.getElementById("arrival-date-end-filter");
    arrivalTimeStartFilter = document.getElementById("arrival-time-start-filter");
    arrivalTimeEndFilter = document.getElementById("arrival-time-end-filter");

    firstnameFilter.addEventListener("input", () => filterAndDisplayRows());
    lastnameFilter.addEventListener("input", () => filterAndDisplayRows());
    companyFilter.addEventListener("input", () => filterAndDisplayRows());
    carFilter.addEventListener("input", () => filterAndDisplayRows());
    arrivalDateStartFilter.addEventListener("input", () => filterAndDisplayRows());
    arrivalDateEndFilter.addEventListener("input", () => filterAndDisplayRows());
    arrivalTimeStartFilter.addEventListener("input", () => filterAndDisplayRows());
    arrivalTimeEndFilter.addEventListener("input", () => filterAndDisplayRows());

    filterAndDisplayRows();
});

function displayArrivals(arrivals) {
    arrivalsTableBody.innerHTML = '';

    for (let arrival of arrivals) {
        let row = document.createElement("tr");

        row.appendChild(createTextTableField(arrival.id, true));
        row.appendChild(createTextTableField(arrival.name));
        row.appendChild(createTextTableField(arrival.company));
        row.appendChild(createTextTableField(arrival.register_number));
        row.appendChild(createTextTableField(arrival.arrival_timestamp));
        row.appendChild(createTextTableField(arrival.leave_timestamp));
        row.appendChild(createTextTableField(arrival.description));
        
        let long_text_container = document.createElement("div");
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

        arrivalsTableBody.appendChild(row);
    }
}

function filterAndDisplayRows() {
    let filtered = filterRows(
        historyArrivals, 
        [
            firstnameFilter.value,
            lastnameFilter.value,
            companyFilter.value,
            carFilter.value,
            arrivalDateStartFilter.value,
            arrivalDateEndFilter.value,
            arrivalTimeStartFilter.value,
            arrivalTimeEndFilter.value
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
    displayArrivals(filtered);
}
