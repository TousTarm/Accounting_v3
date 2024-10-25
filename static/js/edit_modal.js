document.addEventListener('DOMContentLoaded', function() {
    const typeFlagButtons = document.querySelectorAll('.type, .flag');
    const modal = document.getElementById('modal');
    const modalOverlay = document.getElementById('modal_overlay');

    // Event listener for type/flag buttons
    typeFlagButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const objectId = event.target.value;
            // Show modal and overlay
            modal.style.display = 'flex';
            modalOverlay.style.display = 'flex';

            // Fetch data from the server
            fetch(`/get_data/${objectId}`)
            .then(response => {
                return response.text(); // Get raw response text
            })
            .then(rawText => {
                return JSON.parse(rawText); // Parse the raw text as JSON
            })
            .then(data => {
                modal.innerHTML = `
                    <form method="post" class="update_form bg-blue-500 flex" action="/update_data">
                        <input type="hidden" name="id" value="${data._id}"/>
                        <input type="text" name="date" class="field text-sm rounded-lg p-[4px]" placeholder="dd.mm.yyyy" value="${data.date}"/>
                        <input type="text" name="amount" class="field text-sm rounded-lg p-[4px]" placeholder="Amount" value="${data.amount}"/>
                        <input type="text" name="account" class="field text-sm rounded-lg p-[4px]" placeholder="Account" value="${data.account}"/>
                        <textarea name="note" class="field-note text-sm rounded-lg p-[4px]" placeholder="Note" rows="4">${data.note}</textarea>
                        <div class="dropdown-container">
                            <div id="type-button" onclick="open_dropdown('type')">${data.type}</div>
                            <div id="dropdown-content-type" style="display: none;"></div>
                            <input type="hidden" name="type" id="type-input">
                        </div>
                        <div class="dropdown-container">
                            <div id="flag-button" onclick="open_dropdown('flag')">${data.flag}</div>
                            <div id="dropdown-content-flag" style="display: none;"></div>
                            <input type="hidden" name="flag" id="flag-input">
                        </div>

                        <button class="bg-white text-black w-[70px] h-[25px]" type="submit">Submit</button>
                    </form>
                    `;
            })
            .catch(error => console.error('Error fetching data:', error));

                });
            });

    modalOverlay.addEventListener('click', function(event) {
        if (event.target === modalOverlay) {
            modal.style.display = 'none';
            modalOverlay.style.display = 'none';
        }
    });
});
