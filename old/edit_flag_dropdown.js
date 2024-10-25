function open_flag_dropdown() {
    const dropdownContent = document.getElementById('dropdown-content-flag');
    const flagBtn = document.getElementById("flag-btn");
    const flagInput = document.getElementById("flag-input");

    if (dropdownContent.children.length === 0) {
        fetch('/get_keywords?type=flag')  // Specify "flag" as the type
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(flags => {
                dropdownContent.innerHTML = '';
                if (flags.length === 0) {
                    dropdownContent.innerHTML = '<p>No flags available</p>';
                } else {
                    flags.forEach(flag => {
                        const div = document.createElement('div');
                        div.innerText = flag.name;
                        div.classList.add("select-flag");
                        div.addEventListener("click", () => {
                            flagBtn.innerText = flag.name;
                            flagInput.value = flag.name;
                            dropdownContent.style.display = 'none';
                            flagBtn.style.display = 'block';
                        });
                        dropdownContent.appendChild(div);
                    });
                    dropdownContent.style.display = 'block';
                    flagBtn.style.display = "none";
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    } else {
        dropdownContent.style.display = (dropdownContent.style.display === 'none' || dropdownContent.style.display === '') ? 'block' : 'none';
    }
}
