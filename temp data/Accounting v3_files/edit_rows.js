function showTypes(rowID){
    console.log("clicked on", rowID);
    fetch('/get_type')
    .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
    })
    .then(data => {
    console.log(data);
    const container = document.getElementById(rowID);
    data.forEach(item => {
        const div = document.createElement('div');
        div.textContent = item.type;
        div.classList.add("type");
        container.appendChild(div);
        container.style.display = "fixed";
    });
    })
    .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
    });
}