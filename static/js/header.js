const memberToken = localStorage.getItem('memberToken');
const newMemberToken = document.getElementById('memberToken').value
if (memberToken) {
    searchUserInfo(memberToken)
} else {
    if (!!newMemberToken) {
        localStorage.setItem('memberToken', newMemberToken) 
        searchUserInfo(newMemberToken)
    } else {
        window.location = '/login'
    }
}



function searchUserInfo(memberToken) {
    fetch('/api/searchUserInfo', {
        headers: new Headers({
            "Authorization": memberToken,
        })
    })
    .then(async (response) => {
        const status = response.status
        if (status == 200) {
            const responseData = await response.json()
            const userInfo = responseData['data']
            console.log(userInfo)
            if (userInfo) {
                const loginUserDiv = document.getElementById('loginUser')
                loginUserDiv.style.display = 'flex';
                const picUrl = userInfo['profile_pic_url'];
                if (picUrl) {
                    loginUserDiv.style.backgroundImage = 'url(' + picUrl + ')';
                }
            }
        }
    })
}

document.getElementById('liveNowCalendar').addEventListener('click', function() {
    initCalendarHtml();
});

document.getElementById('myArtists').addEventListener('click', function() {
    const memberToken = localStorage.getItem('memberToken');
    if (memberToken) {
        // 驗證token
        window.location = '/myArtists'
    } else {
        window.location = '/login'
    }
    // initArtistHtml();
});