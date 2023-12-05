function initLineLoginBtn() {
    document.getElementById('lineLoginBtn').addEventListener('click', function() {
        console.log('Line login');
        let redirectUri = encodeURIComponent('https://live-now.jc-chen.online');
        let para = 'response_type=code&client_id=2001941861&redirect_uri=' + redirectUri + '&state=12345aXXXbcde&scope=profile%20openid%20email&nonce=09876xyz'
        window.open('https://access.line.me/oauth2/v2.1/authorize?' + para, target = '_self')
    });
}

// function initGoogleLoginBtn() {
//     document.getElementById('googleLoginBtn').addEventListener('click', function(googleUser) {
//         var profile = googleUser.getBasicProfile();
//         console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
//         console.log('Name: ' + profile.getName());
//         console.log('Image URL: ' + profile.getImageUrl());
//         console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
//     });
// }


window.onload = function () {
    google.accounts.id.initialize({
      client_id: '342638350102-cde2d515jvn80bo5m4j8u411fctjhh7n.apps.googleusercontent.com',
      login_uri: 'https://live-now.jc-chen.online/',
      callback: function(CredentialResponse) {
            let credential = CredentialResponse.credential
            console.log(credential);
      }
    });
    google.accounts.id.prompt();
};

initLineLoginBtn();