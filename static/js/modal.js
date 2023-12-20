
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

function fillUpModalContent(contentElements) {
    let modalContent = document.getElementById('modalContent');
    if (modalContent) {
        // 將modale content的卷軸重置到頂端
        modalContent.scrollTop = 0;
       // 將modale content清空
        modalContent.innerHTML = null;
        modalContent.appendChild(contentElements);
    }
}

window.onclick = function(event) {
    const modal = document.getElementById('modalContainer')
    // !event.detail || event.detail == 1 防止雙擊畫面
    if ((!event.detail || event.detail == 1) && event.target == modal) {
        console.log('window click');
        closeModal();
    }
}


initCloseModalBtn();