let handleConcertTime = async function(response) {
    if (response.status == 200) {
        let result = await response.json();
        data = result['data']
        removeCalendarEvent(data);
        return data
    } else {
        return null
    }
}

let removeCalendarEvent = async function(data) {
    if (data) {
        for (let i=0; i < data.length; i++) {
            let concert_time_table_id = data[i]['concert_time_table_id'];
            let calendarEvent  = calendar.getEventById(concert_time_table_id);
            if (calendarEvent) {
                calendarEvent.remove();
            }
        }
    }
}

let refreshCalendarEvent = function(data) {
    if (data) {
        for (let i=0; i < data.length; i++) {
            let concert_time_table_id = data[i]['concert_time_table_id'];
            let startDate = new Date(data[i]['concert_time_table_datetime'] + '+8')
            let endDate = new Date(data[i]['concert_time_table_datetime'] + '+8')
            endDate.setTime(endDate.getTime() + 1 * 60 * 60 * 1000);
            let item = {
                id: concert_time_table_id,
                groupId:data[i]['concert_info_id'],
                title: data[i]['concert_info_name'],
                start: startDate, 
                end: endDate,
                borderColor:data[i]['concert_time_table_type'] == '售票時間' ? 'red' : 'blue'
            }
            // console.log(item)
            calendar.addEvent(item);
        }
    }
}
function queryConcertTimeDataByTimePeriod(calendar, startDate, endDate) {
    fetch('../api/calendar/queryConcertTimeDataByTimePeriod?startDate=' + startDate + "&endDate=" + endDate)
    .then(handleConcertTime)
    .then((data) => {
        // console.log(data)
        refreshCalendarEvent(data)
    })
    .catch((err) => {
        console.log(err);
    });
}
let calendar;
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
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

        // events: [
        //     {   id: 1,
        //         groupId:1,
        //         title: 'MC HotDog熱狗「髒藝術家」2023台北小巨蛋演唱會', // a property!
        //         start: '2023-11-04T11:00:00', // a property!
        //         end: '2023-11-04T12:00:00'
        //     },
        //     {   id: 2,
        //         groupId:1,
        //         title: 'MC HotDog熱狗「髒藝術家」2023台北小巨蛋演唱會', // a property!
        //         start: '2023-11-04T13:00:00', 
        //         end: '2023-11-04T14:00:00',
        //         borderColor:'red',
        //         backgroundColor: '#ff0000'
        //     }
        // ]
    });
    // https://fullcalendar.io/docs/Calendar-addEvent
    // calendar.addEvent({
    //     id: 3,
    //     groupId:2,
    //     title: '2023 徐佳瑩',
    //     start: '2023-11-05T17:00:00', 
    //     end: '2023-11-05T16:00:00',
    //     borderColor:'red',
    //     backgroundColor: '#ff0000'
    // });
    calendar.on('dateClick', function(info) {
        console.log('dateClick: ');
        console.log('dateStr ' + info.dateStr);
        // info.dayEl.className = 'calendar-date-hover-color'
        // console.log('activeEnd ' + info.activeEnd);
        // console.log('currentStart ' + info.currentStart);
        // console.log('currentEnd ' + info.currentEnd);
      });

    // https://fullcalendar.io/docs/datesSet
    calendar.on('datesSet', function(dateInfo) {
        // console.log('datesSet: ');
        // console.log('datesSet ' + dateInfo.startStr);
        // console.log('datesSet ' + dateInfo.endStr);
        queryConcertTimeDataByTimePeriod(calendar, dateInfo.startStr, dateInfo.endStr)
    })
    calendar.render();

   
    console.log(calendar.getOption('locale'))
});