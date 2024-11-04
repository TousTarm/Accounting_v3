function open_dropdown(dropdownType) {
    const dropdownContent = document.getElementById(`dropdown-content-${dropdownType}`);
    const btn = document.getElementById(`${dropdownType}-button`);
    const input = document.getElementById(`${dropdownType}-input`);

    // Open dropdown and load content if not already populated
    if (dropdownContent.children.length === 0) {
        fetch(`/get_${dropdownType}`)  // Adjusted to fetch based on dropdownType
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(items => {
                dropdownContent.innerHTML = '';
                const uniqueValues = [...new Set(items.map(item => item[dropdownType]))];

                if (uniqueValues.length === 0) {
                    dropdownContent.innerHTML = `<p>No ${dropdownType}s available</p>`;
                } else {
                    uniqueValues.forEach(value => {
                        const div = document.createElement('div');
                        div.innerText = value;
                        div.classList.add(`select-button`);
                        div.addEventListener("click", (e) => {
                            e.stopPropagation();  // Prevents this click from triggering document click
                            btn.innerText = value;
                            input.value = value;
                            dropdownContent.style.display = 'none';
                            btn.style.display = 'block';
                        });
                        dropdownContent.appendChild(div);
                    });
                    dropdownContent.style.display = 'block';
                    btn.style.display = "none";
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    } else {
        dropdownContent.style.display = (dropdownContent.style.display === 'none' || dropdownContent.style.display === '') ? 'block' : 'none';
    }

    function handleOutsideClick(event) { // Function to close the dropdown if clicked outside
        if (!dropdownContent.contains(event.target) && event.target !== btn) {
            dropdownContent.style.display = 'none';
            btn.style.display = 'block';
            document.removeEventListener('click', handleOutsideClick);
        }
    }
    setTimeout(() => document.addEventListener('click', handleOutsideClick), 0); // Attach the outside click listener
}
