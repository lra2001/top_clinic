document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('id_date');
    const specialtyInput = document.getElementById('id_specialty');
    const slotsDiv = document.getElementById('available-slots');
    const timeField = document.getElementById('id_time');

    if (!dateInput || !specialtyInput || !slotsDiv) return;

    // Set today's date as min
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);

    async function loadSlots() {
        const date = dateInput.value;
        const specialty = specialtyInput.value;
        if (!date || !specialty) return;

        try {
            const response = await fetch(`/ajax/get-available-slots/?date=${date}&specialty=${specialty}`);
            const data = await response.json();

            // Clear previous content
            slotsDiv.innerHTML = '';

            if (data.error) {
                slotsDiv.innerHTML = `<p class="text-danger">${data.error}</p>`;
                return;
            }

            if (data.slots.length === 0) {
                slotsDiv.innerHTML = `<p class="text-muted">No available slots for this date.</p>`;
                return;
            }

            // Add buttons for each slot
            data.slots.forEach(slot => {
                const button = document.createElement('button');
                button.type = 'button';
                button.textContent = slot.time;
                button.className = `btn btn-sm m-1 ${slot.available ? 'btn-outline-success' : 'btn-secondary'}`;
                button.disabled = !slot.available;

                if (slot.available) {
                button.addEventListener('click', () => {
                    // Set hidden time field
                    timeField.value = slot.time;

                    // Ensure the value exists in the select element
                    let option = Array.from(timeField.options).find(opt => opt.value === slot.time);
                    if (!option) {
                        option = new Option(slot.time, slot.time, true, true);
                        timeField.appendChild(option);
                    }

                    // Remove highlight from other buttons
                    slotsDiv.querySelectorAll('button').forEach(b => b.classList.remove('btn-success'));
                    button.classList.remove('btn-outline-success');
                    button.classList.add('btn-success');
                });
            }

                slotsDiv.appendChild(button);
            });
        } catch (err) {
            slotsDiv.innerHTML = `<p class="text-danger">Error loading slots.</p>`;
            console.error(err);
        }
    }

    dateInput.addEventListener('change', loadSlots);
    specialtyInput.addEventListener('change', loadSlots);
});