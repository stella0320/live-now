
function generateConcertInfoTime(contentDiv, timeDataList) {
    if (timeDataList && timeDataList.length > 0) {
        let timeDiv = document.createElement('div');
        timeDiv.classList.add('concert-info-content-item-time');
        
        for (let i = 0; i < timeDataList.length ; i++) {
            timeData = timeDataList[i];
            let subTimeDiv = document.createElement('div');
            subTimeDiv.classList.add('concert-info-content-item-time-subitem');

            let time = timeData['concert_time_table_datetime'];
            let concertTimeDiv = document.createElement('div');
            concertTimeDiv.classList.add('concert-info-content-item-time-subitem-time');
            concertTimeDiv.classList.add('concert-info-content-item-text-style');
            let timeText = document.createTextNode(time);
            concertTimeDiv.appendChild(timeText);
            subTimeDiv.appendChild(concertTimeDiv);

            let desc = timeData['concert_time_table_description'];
            if (desc) {
                let concertTimeDescDiv = document.createElement('div');
                concertTimeDescDiv.classList.add('concert-info-content-item-time-subitem-desc');
                concertTimeDescDiv.classList.add('concert-info-content-item-text-style');
                let descText = document.createTextNode(desc);
                concertTimeDescDiv.appendChild(descText);
                subTimeDiv.appendChild(concertTimeDescDiv);
            }
            
            
            timeDiv.appendChild(subTimeDiv);
        }
        contentDiv.appendChild(timeDiv);
    }
    

}

function generateConcertInfoContentItem(titleText, contentText) {
    if (!contentText) {
        return;
    }
    let item = document.createElement('div');
    item.classList.add('concert-info-content-item');


    let title = document.createElement('div');
    title.classList.add('concert-info-content-item-title');

    let titleIcon = document.createElement('div');
    titleIcon.classList.add('concert-info-content-item-title-icon');

    let titleIconImage = document.createElement('img');
    titleIconImage.src = "/static/images/icon/singer.png";
    titleIcon.appendChild(titleIconImage);

    let titleTextDiv = document.createElement('div');
    titleTextDiv.classList.add('concert-info-content-item-title-text');

    let titleTextText = document.createTextNode(titleText);
    titleTextDiv.appendChild(titleTextText)
    title.appendChild(titleIcon);
    title.appendChild(titleTextDiv);

    let hr = document.createElement('hr');

    let contentDiv = document.createElement('div');
    contentDiv.classList.add('concert-info-content-item-text');
    contentDiv.classList.add('concert-info-content-item-text-style');

    if (titleText == '售票連結') {
        let a = document.createElement('a');
        a.href = contentText;
        a.target = '_blank';
        let contentTextText = document.createTextNode(contentText);
        a.appendChild(contentTextText);
        contentDiv.appendChild(a);
    } else if (titleText == '售票時間' || titleText == '演出時間') {
        generateConcertInfoTime(contentDiv, contentText);
    } else {
        let contentTextText = document.createTextNode(contentText);
        contentDiv.appendChild(contentTextText);
    }
    


    item.appendChild(title);
    item.appendChild(hr);
    item.appendChild(contentDiv);
    return item;
}



function generateConcertInfoElements(data) {

    let container = document.createElement('div');
    container.classList.add('concert-info-container');

    let coverContainer = document.createElement('div');
    coverContainer.classList.add('concert-info-cover');

    let coverBg = document.createElement('div');
    coverBg.classList.add('concert-info-cover-bg');

    let imageUrl = data['concert_info_image_url']
    let coverBgImage = document.createElement('img');
    coverBgImage.classList.add('concert-info-cover-bg-image');
    coverBgImage.src = imageUrl;
    coverBg.appendChild(coverBgImage);
    coverContainer.appendChild(coverBg);

    let coverMain = document.createElement('div');
    coverMain.classList.add('concert-info-cover-main');

    let coverMainImage = document.createElement('img');
    coverMainImage.classList.add('concert-info-cover-main-image');
    coverMainImage.src = imageUrl;
    coverMain.appendChild(coverMainImage);
    coverContainer.appendChild(coverMain);

    let coverTitle = document.createElement('div');
    coverTitle.classList.add('concert-info-cover-title');
    let coverTitleText = document.createElement('div');
    coverTitleText.classList.add('concert-info-cover-title-text');
    let titleName = data['concert_info_name'];
    let titleText = document.createTextNode(titleName);
    coverTitleText.appendChild(titleText);
    coverTitle.appendChild(coverTitleText);
    coverContainer.appendChild(coverTitle);

    // ---------------------------------------------------
    let concertInfoContainer = document.createElement('div');
    concertInfoContainer.classList.add('concert-info-content-container');

    let concertInfoContent = document.createElement('div');
    concertInfoContent.classList.add('concert-info-content');
    concertInfoContainer.appendChild(concertInfoContent);

    let concertInfoContentText = document.createElement('div');
    concertInfoContentText.classList.add('concert-info-content-text');
    concertInfoContent.appendChild(concertInfoContentText);
    let singer = data['singer_info_name'];
    let singerItem = generateConcertInfoContentItem('歌手', singer);
    concertInfoContentText.appendChild(singerItem);
    
    let location = data['concert_location_name'];
    let locationItem = generateConcertInfoContentItem('演出地點', location);
    concertInfoContentText.appendChild(locationItem);

    let concertTime = data['concert_time_list'];
    let concertTimeItem = generateConcertInfoContentItem('演出時間', concertTime);
    concertInfoContentText.appendChild(concertTimeItem);

    let sellTicketTime = data['sell_ticket_time_list'];
    let sellTicketTimeItem = generateConcertInfoContentItem('售票時間', sellTicketTime);
    concertInfoContentText.appendChild(sellTicketTimeItem);

    let systemDomain = data['concert_info_ticket_system_id'] == 1 ? 'https://tixcraft.com' : '';
    let sellTicketLink = systemDomain + data['concert_info_page_url'];
    let sellTicketLinkItem = generateConcertInfoContentItem('售票連結', sellTicketLink);
    concertInfoContentText.appendChild(sellTicketLinkItem);

    container.appendChild(coverContainer);
    container.appendChild(concertInfoContainer);
    return container;
}