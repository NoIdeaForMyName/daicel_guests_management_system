
//const BASE_DATE = "1970-01-01T";
//const TZ_OFFSET = new Date().getTimezoneOffset() * 60000 // in ms

export function createTextTableField(text, hidden=false) {
    let tableNode = document.createElement("td");
    tableNode.textContent = text;
    tableNode.hidden = hidden
    return tableNode;
}

export function createCheckboxTableField(id) {
    const actionTableNode = document.createElement("td");
    actionTableNode.className = "text-center align-middle";

    const checkContainer = document.createElement("div");
    checkContainer.className = "form-check d-inline-block";

    const actionNode = document.createElement("input");
    actionNode.className = "form-check-input m-0 custom-checkbox"; // Dodana klasa
    actionNode.type = "checkbox";
    actionNode.name = "check[]";
    actionNode.value = id;

    actionNode.style.width = "1.5rem";
    actionNode.style.height = "1.5rem";
    actionNode.style.cursor = "pointer";

    checkContainer.appendChild(actionNode);
    actionTableNode.appendChild(checkContainer);

    return actionTableNode;
}

export function filterRows(allArrivals, values, columns) {
    let filteredArrivals = [];

    values = values.map(v => v.trim().toLowerCase());

    for (let arrival of allArrivals) {
        let fulfills = true;
        for (let i=0; i < values.length && fulfills; i++) {
            let value = values[i];
            if (value === '') {
                continue;
            }
            let column = columns[i];
            let columnValue;
            let d;
            switch (column) {
                case 'firstname':
                case 'lastname':
                    columnValue = arrival['name'].split(' ')[column === 'firstname' ? 0 : 1];
                    break;
                case 'date_start':
                    d  = arrival['arrival_timestamp']
                    columnValue = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
                    value = new Date(value).getTime()
                    break;
                case 'time_start':
                    d  = arrival['arrival_timestamp']
                    columnValue = d.getTime();
                    value = new Date(d.getFullYear(), d.getMonth(), d.getDate(), value.split(':')[0], value.split(':')[1]).getTime();
                    break;
                case 'date_end':
                    d  = arrival['leave_timestamp']
                    columnValue = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
                    value = new Date(value).getTime();
                    break;
                case 'time_end':
                    d  = arrival['leave_timestamp']
                    columnValue = d.getTime();
                    value = new Date(d.getFullYear(), d.getMonth(), d.getDate(), value.split(':')[0], value.split(':')[1]).getTime();
                    break;
                default:
                    columnValue = arrival[column];
            }
            if (!columnValue) {
                fulfills = false;
                continue;
            }
            switch (column) {
                case 'date_start':
                case 'time_start':
                    fulfills = columnValue >= value;
                    break;
                case 'date_end':
                case 'time_end':
                    fulfills = columnValue <= value;
                    break;
                default:
                    fulfills = columnValue.toLowerCase().trim().includes(value);
                    break;
            }
        }
        if (fulfills) {
            filteredArrivals.push(arrival);
        }
    }
    return filteredArrivals;
}

