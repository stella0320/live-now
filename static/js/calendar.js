let handleConcertTime = async function(response) {
    if (response.status == 200) {
        let result = await response.json();
        data = result['data']
        removeCalendarEvent();
        return data
    } else {
        return null
    }
}

let removeCalendarEvent = async function() {
    let events = calendar.getEvents();
    if (events) {
        for (let i=0; i < events.length; i++) {
            let event  = events[i]
            event.remove();
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
                    'singerName': data[i]['singer_info_name'],
                    'member_calendar_event_id' : data[i]['member_calendar_event_id']
                }
            }
            // color: https://fullcalendar.io/docs/list-view
            // console.log(item)
            calendar.addEvent(item);
        }
    }
}
async function queryConcertTimeDataByTimePeriod(startDate, endDate, isMycalendar) {
    changeModalLoadingDisplay('block');
    let formData = new FormData();
    formData.append('startDate', startDate);
    formData.append('endDate', endDate);
    formData.append('memberToken', localStorage.getItem('memberToken'));
    formData.append('isMycalendar', isMycalendar);
    fetch('../api/calendar/queryConcertTimeDataByTimePeriod', {
        method:'POST',
        body: formData
    })
    .then(handleConcertTime)
    .then((data) => {
        refreshCalendarEvent(data)
    })
    .catch((err) => {
        console.log(err);
    })
    .finally(() => {
        changeModalLoadingDisplay('none');
    });
}

function formatTwoNumber(number) {
    return (number.length == 1 ? ('0' + number) : number) 
}
function formatDate(date) {
    let month = (date.month + 1).toString()
    let day =  date.day.toString()
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


    let svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '30');
    svg.setAttribute('height', '30');

    let path = document.createElementNS('http://www.w3.org/2000/svg', 'path');  
    path.setAttribute('stroke-linecap', 'round');
    path.setAttribute('stroke-width', '.8');
    path.setAttribute('d', 'M 4.318 6.318 a 4.5 4.5 0 0 0 0 6.364 L 12 20.364 l 7.682 -7.682 a 4.5 4.5 0 0 0 -6.364 -6.364 L 12 7.636 l -1.318 -1.318 a 4.5 4.5 0 0 0 -6.364 0 Z');
    
    const isLoveConcertEvent = extendedProps['member_calendar_event_id']
    if (!!isLoveConcertEvent) {
        path.classList.toggle('svg-icon');
    }
    
    svg.appendChild(path);

    iconContainer.appendChild(iconItemContainer);
    iconItemContainer.appendChild(iconLabel);
    iconLabel.appendChild(svg);

    container.appendChild(titleContainer);

    container.appendChild(iconContainer);
    return container;
}
let calendar;

let initFullCalendar = function(isMycalendar) {
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
        queryConcertTimeDataByTimePeriod(dateInfo.startStr, dateInfo.endStr, isMycalendar)
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
        // console.log('Event: ' + info.event.id);
        const concert_info_hash_id = info.event.groupId
        changeModalLoadingDisplay('block');
        changeModalBlackBackgroudDisplay('block');
        queryConcertInfoByHashId(concert_info_hash_id);
    })
    calendar.addEventSource({
        'backgroundColor': 'background-color: rgba(247, 119, 6 ,0.2);',
    })
    calendar.render();
}

async function queryConcertInfoByHashId(hashId) {
    const member_token= localStorage.getItem('memberToken')
    fetch('/api/concert_info?concert_info_hash_id=' + hashId + "&member_token=" + member_token).then(async (response) => {
        if (response.status == 200) {
            // 跳到結帳頁面
            let result = await response.json();
            let data = result['data']
            let concertInfoElements = generateConcertInfoElements(data);
            fillUpModalContent(concertInfoElements);
        }
    }).then(() => {
        changeModalLoadingDisplay('none');
        openModal('1200px');
    });
}


