function initSearchSingerNameBtn() {
    document.getElementById('searchSingerNameBtn').addEventListener('click', function() {
        const singerName = document.getElementById('singerName').value
        querySingerInfo(singerName)
    })

    
}

function initSearchSingerNameInput() {
    const singerNameInput = document.getElementById("singerName");

    singerNameInput.addEventListener("keypress", function(event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            document.getElementById('searchSingerNameBtn').click();
        }
    });
}

function toggleMemberSingerEvent(singerInfoHashId) {
    const memberToken = localStorage.getItem('memberToken')
    // changeModalLoadingDisplay('block')
    fetch('/api/toggleMemberSingerEvent?memberToken=' + memberToken + '&singerInfoHashId=' + singerInfoHashId)
    .then(async (response) => {
        const status = response.status
        
    })
    .finally(() => {
        // changeModalLoadingDisplay('none')
    })
}


function generateSingerInfoElement(singerInfoList) {
    const myArtistContent = document.getElementById('myArtistContent')
    myArtistContent.innerHTML = ''
    if (singerInfoList && singerInfoList.length > 0) {

        
        for (let i = 0; i < singerInfoList.length ; i++) {

            const container = document.createElement('div')
            container.classList.add('artist-container')
            const singerInfoId = singerInfoList[i]['singer_info_id']
            container.setAttribute('data-id', singerInfoId)

            const imageContainer = document.createElement('div')
            imageContainer.classList.add('artist-image-container')
            const image = document.createElement('div')
            image.classList.add('artist-image')
            imageContainer.appendChild(image)

            const nameContainer = document.createElement('div')
            nameContainer.classList.add('artist-name-container')

            const name = document.createElement('div')
            name.classList.add('artist-name')

            const singerInfoName = singerInfoList[i]['singer_info_name']
            const nameText = document.createTextNode(singerInfoName)
            name.appendChild(nameText)
            // const 
            nameContainer.appendChild(name)
            container.appendChild(imageContainer)
            container.appendChild(nameContainer)

            const memberSingerEventId = singerInfoList[i]['member_singer_event_id']
            if (memberSingerEventId) {
                container.classList.toggle('artist-container-active')
            }
            container.addEventListener('click', function(e) {
                
                const singerInfoHashId = this.getAttribute("data-id");
                this.classList.toggle('artist-container-active')
                toggleMemberSingerEvent(singerInfoHashId)
                
            });
            myArtistContent.appendChild(container)

        }
        
    } else {
        const noDataText = document.createTextNode('無資料，請重新查詢')
        myArtistContent.appendChild(noDataText)
    }
}



function querySingerInfo(singerName) {
    const memberToken = localStorage.getItem('memberToken')
    changeModalLoadingDisplay('block')
    let url = '/api/querySingerInfo?memberToken=' + memberToken;
    if (singerName) {
        url += '&singerName=' + singerName
    }
    fetch(url)
    .then(async (response) => {
       
        const staus = response.status
        if (staus == 200) {
            const responseData = await response.json()
            const singerInfoList = responseData['data']
            generateSingerInfoElement(singerInfoList)
            console.log(singerInfoList)
        }

        
    }).finally((response) => {
        changeModalLoadingDisplay('none')
    })

}

querySingerInfo()
initSearchSingerNameBtn()
initSearchSingerNameInput()