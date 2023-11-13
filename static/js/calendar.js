
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
        headerToolbar: { center: 'dayGridMonth,timeGridWeek' }, // buttons for switching between views
        weekNumbers: true,
        weekNumberClassNames: 'calendar-week-number-style',
        views: {
            dayGridMonth: { 
                titleFormat: { year: 'numeric', month: '2-digit', day: '2-digit' }
            },
            timeGridWeek: { // name of view
                titleFormat: { year: 'numeric', month: '2-digit', day: '2-digit' }
                // other view-specific options here
            }

        },

        events: [
            {   id: 1,
                groupId:1,
                title: 'MC HotDog熱狗「髒藝術家」2023台北小巨蛋演唱會', // a property!
                start: '2023-11-04T11:00:00', // a property!
                end: '2023-11-04T12:00:00'
            },
            {   id: 2,
                groupId:1,
                title: 'MC HotDog熱狗「髒藝術家」2023台北小巨蛋演唱會', // a property!
                start: '2023-11-04T13:00:00', 
                end: '2023-11-04T14:00:00',
                borderColor:'red',
                backgroundColor: '#ff0000'
            }
        ]
    });
    // https://fullcalendar.io/docs/Calendar-addEvent
    calendar.addEvent({
        id: 3,
        groupId:2,
        title: '2023 徐佳瑩',
        start: '2023-11-05T17:00:00', 
        end: '2023-11-05T16:00:00',
        borderColor:'red',
        backgroundColor: '#ff0000'
    });
    calendar.render();
    console.log(calendar.getOption('locale'))
});