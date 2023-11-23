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
                borderColor:data[i]['concert_time_table_type'] == '售票時間' ? 'red' : 'blue',
                extendedProps: {
                    'singerName': data[i]['singer_info_name']
                }
            }
            // color: https://fullcalendar.io/docs/list-view
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

function formatTwoNumber(number) {
    return (number.length == 1 ? ('0' + number) : number) 
}
function formatDate(date) {
    let month = (date.month + 1).toString()
    let day =  date.day.toString().toString()
    return date.year + '/' + formatTwoNumber(month)  + '/' + formatTwoNumber(day)
}

function formatTime(date) {
    let startDate = date.start;
    let hour = startDate.hour.toString();
    let minute = startDate.minute.toString();
    return  formatTwoNumber(hour) + ':' + formatTwoNumber(minute)
}

function createItemInlistWeek(arg) {
    let data = arg.event;
    let extendedProps = arg.event.extendedProps;
    
    let container = document.createElement('div');
    container.classList.add('concert-item-container');


    let titleContainer = document.createElement('div');
    titleContainer.classList.add('concert-item-title');
    let titleSpan = document.createElement('span');
    let titleText = document.createTextNode(data.title);
    titleSpan.appendChild(titleText);
    titleContainer.appendChild(titleSpan);

    
    let iconContainer = document.createElement('div');
    iconContainer.classList.add('concert-item-icon-container');
    
    let iconItemContainer = document.createElement('div');
    iconItemContainer.classList.add('concert-item-icon');

    let iconLabel = document.createElement('label');
    iconLabel.classList.add('love-icon-btn');

    let inputElement = document.createElement('input');
    inputElement.type = 'checkbox';
    inputElement.classList.add('love-icon-hide');
    inputElement.classList.add('love-icon-checkbox');

    let svg = document.createElement('svg');
    svg.setAttribute('width', '40');
    svg.setAttribute('height', '40');

    let path = document.createElement('path');
    path.setAttribute('fill', 'var(--color-svg)');
    path.setAttribute('stroke-linecap', 'round');
    path.setAttribute('stroke-linejoin', 'round');
    path.setAttribute('stroke-width', '.8');
    path.setAttribute('d', 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z');
    svg.appendChild(path);

    // <path fill="var(--color-svg)" stroke-linecap="round" stroke-linejoin="round" stroke-width=".8" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>

    iconContainer.appendChild(iconItemContainer);
    iconItemContainer.appendChild(iconLabel);
    iconLabel.appendChild(inputElement);
    iconLabel.appendChild(svg);

    container.appendChild(titleContainer);

    container.appendChild(iconContainer);
    return container;
}
let calendar;



document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
        initialView: 'listWeek',
        headerToolbar: { center: 'dayGridMonth,dayGridWeek,listWeek'}, // buttons for switching between views
        weekNumbers: true,
        selectable: true,
        weekNumberClassNames: 'calendar-week-number-style',
        navLinks: true,
        contentHeight: 600,
        navLinkDayClick: function(date, jsEvent) {
            console.log('day', date.toISOString());
            console.log('coords', jsEvent.pageX, jsEvent.pageY);
        },
        views: {
            dayGridMonth: { 
                titleFormat: { year: 'numeric', month: 'long'},
                dayMaxEvents:3
            },
            dayGridWeek: {
                titleFormat: function(date) {
                    return formatDate(date.start) + ' - ' + formatDate(date.end);
                },
                eventTimeFormat: formatTime
            },
            listWeek: {
                titleFormat: function(date) {
                    return formatDate(date.start) + ' - ' + formatDate(date.end);
                },
                listDaySideFormat: function(date) {
                    return formatDate(date.date);
                },
                eventContent: function(arg) {
                    
                    let italicEl = createItemInlistWeek(arg)
                    // console.log(italicEl)
                    // italicEl.innerHTML = arg.event.title + '[' + arg.event.extendedProps.singerName + ']'
                    let arrayOfDomNodes = [ italicEl ]
                
                    return { domNodes: arrayOfDomNodes}
                },
                eventDidMount: function(info) {
                    // console.log(info);
                    // info.el.style.height = '70px';
                },
                eventTimeFormat: formatTime
            }

        }    
    });
    
    calendar.on('dateClick', function(info) {
        // console.log('dateClick: ');
        // console.log('dateStr ' + info.dateStr);
        // console.log(info.view.getCurrentData())
        // info.dayEl.className = 'calendar-date-hover-color'
        // console.log('activeEnd ' + info.activeEnd);
        // console.log('currentStart ' + info.currentStart);
        // console.log('currentEnd ' + info.currentEnd);
    });

    calendar.on('select', function(selectionInfo) {
        // console.log(selectionInfo.view.calendar.currentData.getCurrentData());
        // var events = calendar.getEvents();
        // var eventTitles = events.map(function(event) { return event.title });
        // console.log(eventTitles)
        // https://stackoverflow.com/questions/72710251/click-date-event-can-see-all-the-events-on-that-particular-date-using-angular
    })
    
    
    

    // https://fullcalendar.io/docs/datesSet
    calendar.on('datesSet', function(dateInfo) {
        // console.log('datesSet: ');
        // console.log('datesSet ' + dateInfo.startStr);
        // console.log('datesSet ' + dateInfo.endStr);
        queryConcertTimeDataByTimePeriod(calendar, dateInfo.startStr, dateInfo.endStr)
    })

    calendar.on('eventMouseEnter', function(mouseEnterInfo) {
        mouseEnterInfo.el.style = 'font-weight: 900;border:rgb(247, 119, 6) 2px dashed;backgroundColor: rgba(247, 119, 6 ,0.2)';
    
        // console.log(mouseEnterInfo.jsEvent.clientX);
        // console.log(mouseEnterInfo.jsEvent.clientY);
    })

    calendar.on('eventMouseLeave', function(mouseEnterInfo) {
        // https://fullcalendar.io/docs/eventMouseEnter
        mouseEnterInfo.el.style = 'color:black';
    })

    calendar.on('eventClick', function(info) {
        // https://fullcalendar.io/docs/eventMouseEnter
        console.log('Event: ' + info.event.id)
    })
    calendar.addEventSource({
        'backgroundColor': 'background-color: rgba(247, 119, 6 ,0.2);',
    })
    calendar.render();
    
  
   
    
});
