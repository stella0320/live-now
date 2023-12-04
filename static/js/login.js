function initLineLoginBtn() {
    document.getElementById('lineLoginBtn').addEventListener('click', function() {
        console.log('Line login');
        let redirectUri = encodeURIComponent('https://live-now.jc-chen.online');
        let para = 'response_type=code&client_id=2001941861&redirect_uri=' + redirectUri + '&state=12345aXXXbcde&scope=profile%20openid&nonce=09876xyz'
        window.open('https://access.line.me/oauth2/v2.1/authorize?' + para, target = '_self')
    });
}

function getLineToken(code) {

    xhttp.open("POST", "demo_post.asp", true);
    let redirectUri = encodeURIComponent('https://live-now.jc-chen.online');
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("grant_type=authorization_code&code=" + code + "&redirect_uri=" + redirectUri + "&client_id=2001941861&client_secret=6e0c21c2d89688e0966e00d84095d587");


    xhttp.onreadystatechange = function() {
        console.log('state:'+ this.readyState);
        console.log('response:' + this.responseText);
    };
}


initLineLoginBtn();