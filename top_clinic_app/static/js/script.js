document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.querySelector('#id_date');
    const timeSelect = document.querySelector('#id_time');

    function generateTimeSlots(startHour = 9, endHour = 17, interval = 30) {
        const slots = [];
        for (let hour = startHour; hour < endHour; hour++) {
            for (let min = 0; min < 60; min += interval) {
                let h = hour.toString().padStart(2, '0');
                let m = min.toString().padStart(2, '0');
                slots.push(`${h}:${m}`);
            }
        }
        return slots;
    }

    function updateTimeSlots() {
        const selectedDate = dateInput.value;
        if (!selectedDate) return;

        // Clear previous options
        timeSelect.innerHTML = '';

        // Fetch booked slots from your backend (AJAX) or pass as JSON
        const bookedSlots = []; // Example: ['09:00', '10:30']

        const allSlots = generateTimeSlots();
        allSlots.forEach(slot => {
            const option = document.createElement('option');
            option.value = slot;
            option.textContent = slot;
            if (bookedSlots.includes(slot)) {
                option.disabled = true; // Grey out booked slots
            }
            timeSelect.appendChild(option);
        });
    }

    dateInput.addEventListener('change', updateTimeSlots);

    // Initialize slots on page load
    updateTimeSlots();
});
