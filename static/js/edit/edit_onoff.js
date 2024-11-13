function turnONOFF(rowID) {
    const row = document.getElementById("row-" + rowID);
    fetch('/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: rowID })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.new_status === "on") {
            row.classList.add("on");
            row.classList.remove("off");
        } else if (data.new_status === "off") {
            row.classList.add("off");
            row.classList.remove("on");
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
