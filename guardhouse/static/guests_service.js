
const BASE_DATE = "1970-01-01T";
const TZ_OFFSET = new Date().getTimezoneOffset() * 60000 // in ms

export function createTextTableField(text, hidden=false) {
    let tableNode = document.createElement("td");
    tableNode.textContent = text;
    tableNode.hidden = hidden
    return tableNode;
}

export function createCheckboxTableField(id) {
    let actionTableNode = document.createElement("td");
    let actionNode = document.createElement("input");
    actionNode.type = "checkbox";
    actionNode.name = "check[]";
    actionNode.value = id;
    actionTableNode.appendChild(actionNode);
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
            let temp_date;
            switch (column) {
                case 'firstname':
                case 'lastname':
                    columnValue = arrival['name'].split(' ')[column === 'firstname' ? 0 : 1];
                    break;
                case 'date_start':
                    columnValue = new Date(arrival['arrival_timestamp'].split(',')[0].trim()).getTime();
                    value = new Date(value).getTime() + TZ_OFFSET;
                    break;
                case 'time_start':
                    columnValue = new Date(BASE_DATE + arrival['arrival_timestamp'].split(',')[1].trim()).getTime();
                    value = new Date(BASE_DATE + value).getTime();
                    break;
                case 'date_end':
                    columnValue = new Date(arrival['leave_timestamp'].split(',')[0].trim()).getTime();
                    value = new Date(value).getTime() + TZ_OFFSET;
                    break;
                case 'time_end':
                    columnValue = new Date(BASE_DATE + arrival['leave_timestamp'].split(',')[1].trim()).getTime();
                    value = new Date(BASE_DATE + value).getTime();
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

