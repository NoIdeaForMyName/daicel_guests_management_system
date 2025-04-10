import { createTextTableField, filterRows, createHostsTableField } from './js/guests_service.js';
import { getCookie } from './js/script.js'

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

    guestsTable.style.display = guests.length ? "table" : "none";
    noDataInfo.style.display = guests.length ? "none" : "block";

    guests.forEach(guest => {
        const row = document.createElement("tr");

        row.appendChild(createTextTableField(guest.name, false, "fw-bold"));
        row.appendChild(createTextTableField(guest.company));
        row.appendChild(createTextTableField(guest.description, false, "fw-light fst-italic"));

        row.appendChild(createHostsTableField(guest.hosts));

        const actionCell = document.createElement("td");
        actionCell.className = "text-nowrap";

        const actionContainer = document.createElement("div");
        actionContainer.className = "d-flex gap-2";

        const editButton = document.createElement("a");
        editButton.href = `/host/edit_guest/${guest.id}`;
        editButton.className = "btn btn-primary btn-sm";
        editButton.innerHTML = `
            <i class="bi bi-pencil"></i>
            <span class="d-none d-md-inline">Edytuj</span>
        `;

        const deleteForm = document.createElement("form");
        deleteForm.method = 'POST';
        deleteForm.action = `not-confirmed-guests/delete_guest/${guest.id}/`;
        deleteForm.className = "d-inline";
        deleteForm.onsubmit = function() {
            return confirm('Czy napewno chcesz usunąć tę wizytę?');
        };

        const csrfInput = document.createElement("input");
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = getCookie('csrftoken');

        const deleteButton = document.createElement("button");
        deleteButton.type = 'submit';
        deleteButton.className = 'btn btn-danger btn-sm';
        deleteButton.innerHTML = `
            <i class="bi bi-trash"></i>
            <span class="d-none d-md-inline">Usuń</span>
        `;

        deleteForm.appendChild(csrfInput);
        deleteForm.appendChild(deleteButton);
        actionContainer.appendChild(editButton);
        actionContainer.appendChild(deleteForm);
        actionCell.appendChild(actionContainer);
        row.appendChild(actionCell);

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