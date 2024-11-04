function showTypes(rowID) {
    const container = document.getElementById("ty-"+rowID);
    const old = container.innerHTML;

    fetch('/get_type')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            container.innerHTML = '';
            data.forEach(item => {
                const div = document.createElement('div');
                div.textContent = item.type;
                div.classList.add("type", "dropdown-item");
                div.addEventListener("click", () => {
                    updateType(rowID, item.type);
                    container.style.display = "none";
                });
                container.appendChild(div);
            });
            container.style.display = "block";

            // Add event listener to close dropdown on outside click
            document.addEventListener('click', function handleClickOutside(event) {
                if (!container.contains(event.target) && event.target !== container) {
                    container.style.display = "none";
                    document.removeEventListener('click', handleClickOutside);
                    container.innerHTML = old;  // Restore old content
                }
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function updateType(rowID, value) {
    console.log("you clicked on button", rowID, value);
    fetch('/update_type', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: rowID,
            type: value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const container = document.getElementById("type-"+rowID);
        container.innerHTML = value;
        container.classList.remove("manual");
        container.classList.add("updated");
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
