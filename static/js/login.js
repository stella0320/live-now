// function initLineLoginBtn() {
//     document.getElementById('lineLoginBtn').addEventListener('click', function() {
//         console.log('Line login');

//         // https://developers.google.com/identity/openid-connect/openid-connect
//         // state = hashlib.sha256(os.urandom(1024)).hexdigest()
//         // session['state'] = state
//         let redirectUri = encodeURIComponent('https://live-now.jc-chen.online');
//         let para = 'response_type=code&client_id=2001941861&redirect_uri=' + redirectUri + '&state=12345aXXXbcde&scope=profile%20openid%20email&nonce=09876xyz'
//         window.open('https://access.line.me/oauth2/v2.1/authorize?' + para, target = '_self')
//     });

// }

// function initGoogleLogOut() {

//     const button = document.getElementById('signout_button');
//     button.addEventListener('click', function() {
//         console.log('google logout');
//         google.accounts.id.disableAutoSelect();
//     });
// }


// initLineLoginBtn();
// initGoogleLogOut();




let loginModeLinkEvent = function() {
    const loginTitle = document.getElementById('loginTitle');
    const loginBtn = document.getElementById('loginBtn');
    const loginName = document.getElementById('loginNameDiv');
    const loginModeLink = document.getElementById('loginModeLink');
    const loginBtnTxt = loginBtn.getAttribute('value');
    const loginErrorMassge = document.getElementById('loginErrorMassge');
    loginErrorMassge.innerText = '';
    loginErrorMassge.style.color = 'red';
    if (loginBtnTxt == "loginAccount") {
        // 切換成註冊模式
        loginTitle.innerText = '註冊會員帳號';
        // login name
        loginName.style.display = 'block';
        // btn inner text
        loginBtn.innerText = '註冊新帳戶';
        loginBtn.setAttribute('value', 'registrationAccount');
        // mode text
        loginModeLink.innerText = '已經有帳戶了？點此登入';
    } else if (loginBtnTxt == 'registrationAccount') {
        // 切換成登入模式
        loginTitle.innerText = '登入會員帳號';
        loginName.style.display = 'none';
        loginBtn.innerText = '登入帳戶';
        loginBtn.setAttribute('value', 'loginAccount');
        loginModeLink.innerText = '還沒有帳戶？點此註冊';
    }
}

let loginAccountEvent = function() {
    
    const mail = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    changeModalLoadingDisplay('block');
    fetch('/api/user/auth', {
        method: "PUT",
        body: JSON.stringify({
            mail:mail,
            password:password
        }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
    .then(async function(res){
        changeModalLoadingDisplay('none');
        if (res.status == '400') {
            const response = await res.json();
            const loginErrorMassge = document.getElementById('loginErrorMassge');
            loginErrorMassge.innerText = response['message'];
        } else if (res.status == '200') {
            // 存token
            const response = await res.json();
            if (response) {
                localStorage.setItem('memberToken', response['memberToken']);
                let indexLogOutBtn = document.getElementById('indexLogOutBtn');
                indexLogOutBtn.style.display = 'none';
                // location.reload();
                window.location = '/'
            }
        } else {
            console.log('500');
        }
    });
}


let registrationAccountEvent = function() {
    
    const name = document.getElementById('loginName').value;
    const mail = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    fetch('/api/user', {
        method: "POST",
        body: JSON.stringify({
            name:name,
            mail:mail,
            password:password
        }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
    .then(async function(res) {
        document.getElementById('loginErrorMassge').innerText = '';
        const loginErrorMassge = document.getElementById('loginErrorMassge');
        loginErrorMassge.style.color = 'red';
        if (res.status == '400') {
            const response = await res.json();
            
            loginErrorMassge.innerText = response['message'];
        } else if (res.status == '200') {
            document.getElementById('loginModeLink').click();
            const response = await res.text();
            loginErrorMassge.innerText = response;
            loginErrorMassge.style.color = 'green';
        } else {
            console.log('500');
        }
    });
}

let loginBtnEvent = function(e) {
    let btnType = e.target.getAttribute('value');
    if (btnType == "loginAccount") {
        loginAccountEvent();
    } else if (btnType == 'registrationAccount') {
        registrationAccountEvent();
    }
}

const loginModeLink = document.getElementById('loginModeLink');
loginModeLink.addEventListener('click', loginModeLinkEvent);

const loginBtn = document.getElementById('loginBtn');
loginBtn.addEventListener('click', loginBtnEvent);

const loginModal = document.getElementById('loginModal');

const closeModalBtn = document.getElementById('closeModalBtn');

closeModalBtn.addEventListener('click', function() {
    loginModal.style.display = 'none';
    const loginErrorMassge = document.getElementById('loginErrorMassge');
    loginErrorMassge.innerText = '';
    loginErrorMassge.style.color = 'red';
})

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == loginModal) {
        console.log('window click');
        loginModal.style.display = "none";
        const loginErrorMassge = document.getElementById('loginErrorMassge');
        loginErrorMassge.innerText = '';
        loginErrorMassge.style.color = 'red';
    }
}