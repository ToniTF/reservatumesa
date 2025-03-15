var bookings = JSON.parse(document.getElementById('bookings-data').textContent);
var restaurant = JSON.parse(document.getElementById('restaurant').textContent);
var people = document.getElementById('people');
var date = document.getElementById('date');

min_date();
people.addEventListener('change', checkTime);
date.addEventListener('change', checkTime);

function min_date() {
    var dateInput = document.getElementById('date');
    var today = new Date();
    var tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    var dd = String(tomorrow.getDate()).padStart(2, '0');
    var mm = String(tomorrow.getMonth() + 1).padStart(2, '0'); // January is 0!
    var yyyy = tomorrow.getFullYear();
    var minDate = yyyy + '-' + mm + '-' + dd;
    dateInput.setAttribute('min', minDate);
}

function checkTime() {
    var date_value = date.value;
    var people_value = people.value;
    if (date_value && people_value) {

        var time = document.getElementById('time');
        time.innerHTML = ''; // Clear previous options
        var booking_time = new Date(date_value + 'T13:00:00');
        var booking_end = new Date(date_value + 'T15:00:01');
        while (booking_time < booking_end) {
            var available = checkAvailability(booking_time, people_value);
            if (available) {
                time.innerHTML += '<option value="' + booking_time.toTimeString().slice(0, 5) + '">' + booking_time.toTimeString().slice(0, 5) + '</option>';
            }
            booking_time.setMinutes(booking_time.getMinutes() + 30); // Incrementar el tiempo en 30 minutos
        }
        booking_time = new Date(date_value + 'T20:00:00');
        booking_end = new Date(date_value + 'T23:00:01');
        while (booking_time < booking_end) {
            var available = checkAvailability(booking_time, people_value);
            if (available) {
                time.innerHTML += '<option value="' + booking_time.toTimeString().slice(0, 5) + '">' + booking_time.toTimeString().slice(0, 5) + '</option>';
            }
            booking_time.setMinutes(booking_time.getMinutes() + 30); // Incrementar el tiempo en 30 minutos
        }
    }
}

function checkAvailability(booking_time, people) {
    var available = true;
    var booking_time_minus_90 = new Date(booking_time.getTime() - 90 * 60000); // Restar 90 minutos
    var booking_time_plus_90 = new Date(booking_time.getTime() + 90 * 60000); // Añadir 90 minutos
    var people_before = 0;
    var people_after = 0;

    bookings.forEach(function(booking) {
        var booking_start = new Date(booking.date);
        var [hours, minutes] = booking.time.split(':').map(Number);
        booking_start.setHours(hours, minutes);
        if (booking_start <= booking_time && booking_start >= booking_time_minus_90) {
            people_before += booking.diners;
        }
        if (booking_start >= booking_time && booking_start <= booking_time_plus_90) {
            people_after += booking.diners;
        }
    });
    capacity=restaurant.capacity;
    if ((people_before + parseInt(people) > capacity) || (people_after + parseInt(people) > capacity)) {
        available = false;
    }
    return available;
}

