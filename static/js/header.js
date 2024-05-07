const memberToken = localStorage.getItem('memberToken');
const newMemberToken = document.getElementById('memberToken').value

if (memberToken) {
    searchUserInfo(memberToken)
    indexLogOutView()
} else {
    if (!!newMemberToken) {
        localStorage.setItem('memberToken', newMemberToken) 
        searchUserInfo(newMemberToken)
        indexLogOutView()
    } else {
        indexLoginBtn();
        indexLoginView();
    }
}

function indexLoginView() {
    let indexLogOutBtn = document.getElementById('indexLogOutBtn');
    indexLogOutBtn.style.display = 'none';
    let indexLogInBtn = document.getElementById('indexLoginBtn');
    indexLogInBtn.style.display = 'display';
}

function indexLogOutView() {
    let indexLogOutBtn = document.getElementById('indexLogOutBtn');
    indexLogOutBtn.style.display = 'display';
    let indexLogInBtn = document.getElementById('indexLoginBtn');
    indexLogInBtn.style.display = 'none';
}

function indexLoginBtn() {
    document.getElementById('indexLoginBtn').addEventListener('click', function() {
        loginModal.style.display = 'block';
        
    })
}

function indexLogoutBtn() {
    document.getElementById('indexLogOutBtn').addEventListener('click', function() {
        localStorage.removeItem('memberToken');
        window.location = '/'
        return;
    });
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
    const memberToken = localStorage.getItem('memberToken');
    if (memberToken) {
        // 驗證token
        window.location = '/'
    } else {
        // window.location = '/login'
    }
});

document.getElementById('myCalendar').addEventListener('click', function() {
    const memberToken = localStorage.getItem('memberToken');
    if (memberToken) {
        // 驗證token
        window.location = '/myCalendar'
    } else {
        loginModal.style.display = 'block';
    }
});

// document.getElementById('myArtists').addEventListener('click', function() {
//     const memberToken = localStorage.getItem('memberToken');
//     if (memberToken) {
//         // 驗證token
//         window.location = '/myArtists'
//     } else {
//         // window.location = '/login'
//     }
// });

indexLogoutBtn();