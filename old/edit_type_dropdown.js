function open_type_dropdown() {
    const dropdownContent = document.getElementById('dropdown-content-type');
    const typeBtn = document.getElementById("type-btn");
    const typeInput = document.getElementById("type-input");

    if (dropdownContent.children.length === 0) {
        fetch('/get_keywords?type=type')  // Add the query parameter to specify "type"
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(keywords => {
                dropdownContent.innerHTML = '';
                if (keywords.length === 0) {
                    dropdownContent.innerHTML = '<p>No keywords available</p>';
                } else {
                    keywords.forEach(keyword => {
                        const div = document.createElement('div');
                        div.innerText = keyword.type;
                        div.classList.add("select-type");
                        div.addEventListener("click", () => {
                            typeBtn.innerText = keyword.type;
                            typeInput.value = keyword.type;
                            dropdownContent.style.display = 'none';
                            typeBtn.style.display = 'block';
                        });
                        dropdownContent.appendChild(div);
                    });
                    dropdownContent.style.display = 'block';
                    typeBtn.style.display = "none";
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    } else {
        dropdownContent.style.display = (dropdownContent.style.display === 'none' || dropdownContent.style.display === '') ? 'block' : 'none';
    }
}
