console.log("js loaded");

document.addEventListener('DOMContentLoaded', function() {
    const typeFlagButtons = document.querySelectorAll('.type, .flag');
    const modal = document.getElementById('modal');
    const modalOverlay = document.getElementById('modal_overlay');

    // Event listener for type/flag buttons
    typeFlagButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const objectId = event.target.value;
            console.log("Button clicked with Object ID:", objectId);

            // Show modal and overlay
            modal.style.display = 'flex';
            modalOverlay.style.display = 'flex';

            // Fetch data from the server
            fetch(`/get_data/${objectId}`)
            .then(response => {
                console.log("Response Status:", response.status); // Log response status
                return response.text(); // Get raw response text
            })
            .then(rawText => {
                console.log("Raw Response:", rawText); // Log raw response
                return JSON.parse(rawText); // Parse the raw text as JSON
            })
            .then(data => {
                modal.innerHTML = `
                    <form method="post" class="update_form" action="/update_data">
                        <input type="hidden" name="id" value="${data._id}"/> <!-- Assuming data._id contains the ObjectId -->
                        <input type="text" name="date" class="field text-sm rounded-lg p-[4px]" placeholder="dd.mm.yyyy" value="${data.date}"/>
                        <input type="text" name="amount" class="field text-sm rounded-lg p-[4px]" placeholder="Amount" value="${data.amount}"/>
                        <input type="text" name="account" class="field text-sm rounded-lg p-[4px]" placeholder="Account" value="${data.account}"/>
                        <textarea name="note" class="field-note text-sm rounded-lg p-[4px]" placeholder="Note" rows="4">${data.note}</textarea>
                        <input type="text" name="type" class="field text-sm rounded-lg p-[4px]" placeholder="Type" value="${data.type}"/>
                        <input type="text" name="flag" class="field text-sm rounded-lg p-[4px]" placeholder="Flag" value="${data.flag}"/>
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
