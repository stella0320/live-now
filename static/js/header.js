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
                loginUserDiv.setAttribute('data-id', userInfo['member_hash_id'])
                loginUserDiv.style.display = 'flex';
                const picUrl = userInfo['profile_pic_url'];
                if (picUrl) {
                    loginUserDiv.style.backgroundImage = 'url(' + picUrl + ')';
                } else {
                    loginUserDiv.style.backgroundImage = 'url(/static/images/icon/user.png)';
                }
            }
        }
    })
}

document.getElementById('liveNowCalendar').addEventListener('click', function() {
    // initCalendarHtml();
    const memberToken = localStorage.getItem('memberToken');
    if (memberToken) {
        // 驗證token
        window.location = '/'
    } else {
        window.location = '/login'
    }
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