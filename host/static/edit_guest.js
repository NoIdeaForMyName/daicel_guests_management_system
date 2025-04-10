document.addEventListener("DOMContentLoaded", () => {
    const arrivalData = JSON.parse(document.getElementById('arrival_data_json').textContent);
    if (arrivalData && arrivalData.id) {
        // Wypełnij dodatkowe pola specyficzne dla edycji

        // Dodaj ukryte pole z ID przyjazdu
        const hiddenIdInput = document.createElement('input');
        hiddenIdInput.type = 'hidden';
        hiddenIdInput.id = 'arrival-id';
        hiddenIdInput.value = arrivalData.id;
        document.getElementById('main-form').prepend(hiddenIdInput);

        // Modyfikuj funkcję wysyłającą dane
        window.postGuestData = function() {
            const arrivalId = document.getElementById('arrival-id').value;
            let companyValue = companyNameInput.value;
            let registerNbValue = registerNumberInput.value;
            let descriptionValue = descriptionInput.value;
            let hostsValues = getDataFromTable(hostTableInput);

            if (!validateRegisterNb(registerNbValue)) {
                alert("Nieprawidłowy numer tablicy rejestracyjnej!");
                registerNumberInput.textContent = "";
                return;
            }

            if (descriptionValue.length === 0) {
                alert("Nie podano celu przybycia");
                return;
            }

            if (hostsValues.length === 0) {
                alert("Musisz wprowadzić dane przynajmniej jednego gospodarza!");
                return;
            }

            const confirmMsg = `Czy napewno chcesz zaktualizować dane gościa?`
            if (confirm(confirmMsg)) {
                sendFormToServer({
                    'arrival_id': arrivalId,
                    'confirmed': confirmed_json,
                    'company': companyValue,
                    'register_number': registerNbValue,
                    'description': descriptionValue,
                    'hosts': hostsValues.map(host => ({'id': Number(host[0]), 'firstname': host[1], 'lastname': host[2]})),
                })
                //.then(response => response.json())
                .then(data => {
                    window.location.href = redirect_url;
                })
                .catch(error => {
                    alert(`Error: ${error.message.slice(1, -1)}`);
                });
            }
        }
    }
});
