function initLineLoginBtn() {
    document.getElementById('lineLoginBtn').addEventListener('click', function() {
        console.log('Line login');

        // https://developers.google.com/identity/openid-connect/openid-connect
        // state = hashlib.sha256(os.urandom(1024)).hexdigest()
        // session['state'] = state
        let redirectUri = encodeURIComponent('https://live-now.jc-chen.online');
        let para = 'response_type=code&client_id=2001941861&redirect_uri=' + redirectUri + '&state=12345aXXXbcde&scope=profile%20openid%20email&nonce=09876xyz'
        window.open('https://access.line.me/oauth2/v2.1/authorize?' + para, target = '_self')
    });

}

function initGoogleLogOut() {

    const button = document.getElementById('signout_button');
    button.addEventListener('click', function() {
        console.log('google logout');
        google.accounts.id.disableAutoSelect();
    });
}


initLineLoginBtn();
initGoogleLogOut();