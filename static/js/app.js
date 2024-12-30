const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

let pswrd = document.querySelector('#myInput');
let form_container = document.querySelector('.forms-container');

function strength(password){

  let i = 0 ;
  if(password.length > 6){
    i++;
  }
  if(password.length > 8){
    i++;
  }
  if(/(?=.*[A-Z].*[A-Z])/.test(password)){
    i++;
  }
  if(/(?=.*[!@#$&*])/.test(password)){
    i++;
  }
  if(/(?=.*[0-9].*[0-9])/.test(password)){
    i++;
  }
  if(/(?=.*[a-z].*[a-z].*[a-z])/.test(password)){
    i++;
  }
  if(/.{8}/.test(password)){
    i++;
  }
  return i;
}

document.addEventListener('keyup', function(e){
  let password = document.querySelector('#myInput1').value
  let passwordStrength = strength(password);

  if(passwordStrength <= 3){
    form_container.classList.add('weak');
    form_container.classList.remove('medium');
    form_container.classList.remove('strong');
  }
  else if(passwordStrength >= 3 && passwordStrength <= 5){
    form_container.classList.remove('weak');
    form_container.classList.add('medium');
    form_container.classList.remove('strong');
  }
  else{
    form_container.classList.remove('weak');
    form_container.classList.remove('medium');
    form_container.classList.add('strong');
  }
});

function myFunction() {
  var x = document.getElementById("myInput");
  var y = document.getElementById("myInput1");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
  if (y.type === "password") {
    y.type = "text";
  } else {
    y.type = "password";
  }
}

