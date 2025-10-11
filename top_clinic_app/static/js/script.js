document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.querySelector('#id_date');
    const specialtySelect = document.querySelector('#id_specialty');
    const timeSelect = document.querySelector('#id_time');

    function fetchAvailableSlots() {
        const date = dateInput.value;
        const specialty = specialtySelect.value;
        if (!date || !specialty) return;

        fetch(`/ajax/get-available-slots/?date=${date}&specialty=${specialty}`)
            .then(response => response.json())
            .then(data => {
                timeSelect.innerHTML = '';
                data.slots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.time;
                    option.textContent = slot.time;
                    if (!slot.available) {
                        option.disabled = true;
                        option.textContent += " (Booked)";
                    }
                    timeSelect.appendChild(option);
                });
            });
    }

    dateInput.addEventListener('change', fetchAvailableSlots);
    specialtySelect.addEventListener('change', fetchAvailableSlots);

    // Initialize on page load
    fetchAvailableSlots();
});