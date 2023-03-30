

let menuText = document.querySelectorAll('.batch-bar p');

function Shrink() {
    menuText.forEach(element => {
        element.classList.toggle('hide');
        document.querySelector('.aside-menu-container').classList.toggle('aside-full-width');
        console.log('working!!');
    });
}


let dateInput = document.querySelectorAll("input[name='date']");
dateInput.forEach((input) => {
    input.addEventListener('focus', ()=>{
        input.type = "date";
    })
})

function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

//   function searchFunc() {
//     document.querySelector('.full-search-container').style.display = 'flex';
//   }

const date = new Date();

let day = date.getDate();
let month = date.getMonth() + 1;
let year = date.getFullYear();

function setDefaultDate() {
  document.getElementById("date-filter").defaultValue = `${year}-${month}-${day}`;
}
let currentDate = document.getElementById("date-filter").value
console.log(currentDate);