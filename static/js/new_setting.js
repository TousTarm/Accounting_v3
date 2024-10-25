function addNewField(type) {
    // Create a new div for the form input
    const newDiv = document.createElement('div');
    newDiv.className = "flex setting-row border-white border-[1px]";

    // Create input element
    const inputField = document.createElement('input');
    inputField.type = "text";  // Set the type of input
    inputField.placeholder = type === 'type' ? "Enter new type" : "Enter new flag";  // Set placeholder text
    inputField.className = "bg-black text-white w-1/2 p-2"; // Add Tailwind classes for styling

    // Create a button to submit the new value
    const submitButton = document.createElement('button');
    submitButton.innerText = "Submit";
    submitButton.className = "bg-black text-white w-1/2 p-2 mx-2"; // Add Tailwind classes for styling
    submitButton.onclick = function() {
        const inputValue = inputField.value.trim();  // Get the input value and trim whitespace

        if (inputValue) {
            // Define the API endpoint based on type
            const endpoint = type === 'type' ? '/add_type' : '/add_flag';

            // Send a POST request to the backend
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ [type]: inputValue })  // Send the input value as JSON
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                // Instead of alerting, refresh the page upon successful addition
                location.reload();  // Refresh the page
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // You can log the error or handle it here if necessary
            });
        } else {
            alert(`Please enter a valid ${type}.`);  // Alert if input is empty
        }
    };

    // Append the input field and button to the new div
    newDiv.appendChild(inputField);
    newDiv.appendChild(submitButton);

    // Insert the new div before the "+" div
    const settingBox = type === 'type' ? document.getElementById('types-container') : document.getElementById('flags-container');
    const plusDiv = settingBox.querySelector('.plus');
    settingBox.insertBefore(newDiv, plusDiv);
}
