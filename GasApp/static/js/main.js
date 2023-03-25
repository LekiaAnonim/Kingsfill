

let menuText = document.querySelectorAll('.batch-bar p');

function Shrink() {
    menuText.forEach(element => {
        element.classList.toggle('hide');
        document.querySelector('.aside-menu-container').classList.toggle('aside-full-width');
        console.log('working!!');
    });
}