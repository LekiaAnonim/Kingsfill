

let menuText = document.querySelectorAll('.batch-bar p');
let asideContainer = document.querySelector('#aside-menu-container')

function Shrink() {
    menuText.forEach(element => {
        element.classList.toggle('hide');
        asideContainer.classList.toggle('aside-full-width');
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

document.querySelector('.copyright-year').innerText = year

function setDefaultDate() {
  document.getElementById("date-filter").defaultValue = `${year}-${month}-${day}`;
}
let currentDate = document.getElementById("date-filter").value

function showPassword(checkbox) {
  let passwordInput = document.querySelectorAll("input[type='password']");
  passwordInput.forEach((input) => {
      if (checkbox.checked === true) {
          input.type = "text";
      } else {
          input.type = "password";
      }
  })
}