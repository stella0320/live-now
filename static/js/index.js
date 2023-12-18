// Live Now!行事曆頁面 for header.js
function initCalendarHtml() {

    fetch('/calendar')
    .then((response) => {
        changeModalLoadingDisplay('block');
        return response.text();
    }).then((html) => {
        let content = document.getElementById('content');
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, 'text/html');
        let calendarHtml = doc.querySelector('.calendar-frame')
        content.innerHTML = null;
        content.innerHTML = calendarHtml.outerHTML;        
    }).then(() => {
        // from calendar.js
        initFullCalendar();
    }) 
    .catch((error) => {
        console.log(error);
    })
    .finally(() => {
        // from modal.js
        changeModalLoadingDisplay('none');
    });
    
}

function initArtistHtml() {
    fetch('/myArtist')
    .then((response) => {
        // from modal.js
        changeModalLoadingDisplay('block');
        return response.text();
    }).then((html) => {
        let content = document.getElementById('content');
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, 'text/html');
        let myArtistHtml = doc.querySelector('.my-artist-container')
        content.innerHTML = null;
        content.innerHTML = myArtistHtml.outerHTML;        
    })
    .catch((error) => {
        console.log(error);
    })
    .finally(() => {
        // from modal.js
        changeModalLoadingDisplay('none');
    });
}