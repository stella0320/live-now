
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function changeModalBlackBackgroudDisplay(display) {
    let modalBodyList = document.getElementsByClassName('live-now-modal-body');
    if (modalBodyList) {
        modalBody = modalBodyList[0];
        modalBody.style.display = display;
        
    }
}

async function changeModalLoadingDisplay(display) { 
    let modalLoading = document.getElementById('loading');
    if (modalLoading) {
        modalLoading.style.display = display;
    }
}

function initCloseModalBtn() {
    document.getElementById('modalCloseBtn').addEventListener('click', async function() {
        let modalContainerList = document.getElementsByClassName('live-now-modal-container')
        
        if (modalContainerList) {
            modalContainer = modalContainerList[0];
            modalContainer.classList.toggle('live-now-modal-container-active');
        }

        await sleep(0.7 * 1000);
        changeModalBlackBackgroudDisplay('none');

        // 開modal時，顯示body的右側scroll bar
        let body = document.getElementsByTagName('body')[0]
        body.style.overflow = 'auto';
    });
}

function closeModal() {
    document.getElementById('modalCloseBtn').click();
}

async function openModal(modalWidth) {
    
    // let modalBodyList = document.getElementsByClassName('live-now-modal-body')
    // if (modalBodyList) {
    //     modalBody = modalBodyList[0]
    //     modalBody.style.display = 'block';
    // }

    // 開modal時，將body的scroll bar關閉
    let body = document.getElementsByTagName('body')[0]
    body.style.overflow = 'hidden';
    await sleep(0.1 * 1000);
    let modalContainerList = document.getElementsByClassName('live-now-modal-container')
        
        if (modalContainerList) {
            modalContainer = modalContainerList[0];
            modalContainer.style.width = modalWidth;
            modalContainer.classList.toggle('live-now-modal-container-active');
    }
    
}

function fillUpModalContent(innerHTML) {
    let modalContent = document.getElementById('modalContent');
    if (modalContent) {
        // content = document.createTextNode('123<br>12<br>12<br>12<br>12<br>');
        // modalContent.appendChild(content);
        modalContent.innerHTML = innerHTML
    }
}

initCloseModalBtn();