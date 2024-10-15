function open_dropdown() {
    console.log("click registered");
    const dropdownContent = document.getElementById('dropdown-content');

    if (dropdownContent.children.length === 0) {
        fetch('/get_keywords')
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
                        document.getElementById('type-btn').innerText = keyword.type;
                        dropdownContent.style.display = 'none';
                        dropdownContent.appendChild(div);
                    });
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }
    dropdownContent.style.display = (dropdownContent.style.display === 'none' || dropdownContent.style.display === '') ? 'block' : 'none';
}

