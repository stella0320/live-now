function initLineLoginBtn() {
    document.getElementById('lineLoginBtn').addEventListener('click', function() {
        console.log('Line login');
        let redirectUri = encodeURIComponent('https://live-now.jc-chen.online');
        let para = 'response_type=code&client_id=2001941861&redirect_uri=' + redirectUri + '&state=12345aXXXbcde&scope=profile%20openid%20email&nonce=09876xyz'
        window.open('https://access.line.me/oauth2/v2.1/authorize?' + para, target = '_self')
    });
}


initLineLoginBtn();