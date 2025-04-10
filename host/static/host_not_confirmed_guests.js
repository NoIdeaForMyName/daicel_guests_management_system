import { createTextTableField, filterRows } from './js/guests_service.js';
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

        const actionCell = document.createElement("td");

        const editButton = document.createElement('a');
        editButton.href = `/host/edit_guest/${guest.id}`;
        editButton.className = "edit-link";
        editButton.innerHTML = `<button>Edytuj</button>`;
        actionCell.appendChild(editButton);
        //editButton.innerHTML = `<a href="/host/edit_guest/${guest.id}" class="edit-link"><button>Edytuj</button></a>`;

        const deleteForm = document.createElement('form');
        deleteForm.method = 'POST';
        deleteForm.action = `not-confirmed-guests/delete_guest/${guest.id}/`;
        deleteForm.onsubmit = function() {
            return confirm('Czy napewno chcesz usunąć tę wizytę?');
        };

        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = getCookie('csrftoken');

        const deleteButton = document.createElement('button');
        deleteButton.type = 'submit';
        deleteButton.textContent = 'Usuń';
        deleteButton.className = 'delete-link';

        deleteForm.appendChild(csrfInput);
        deleteForm.appendChild(deleteButton);

        actionCell.appendChild(deleteForm);

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