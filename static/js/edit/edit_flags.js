function showFlags(rowID) {
    const container = document.getElementById("fl-"+rowID);
    const old = container.innerHTML;
    fetch('/get_flag')
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
                div.textContent = item.flag;
                div.classList.add("flag", "dropdown-item");
                div.addEventListener("click", () => {
                    updateFlag(rowID, item.flag);
                    container.style.display = "none";
                });
                container.appendChild(div);
            });
            container.style.display = "block";
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

function updateFlag(rowID, value) {
    fetch('/update_flag', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: rowID,
            flag: value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const container = document.getElementById("flag-"+rowID);
        container.innerHTML = value;
        container.classList.remove("manual");
        container.classList.add("updated");
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
