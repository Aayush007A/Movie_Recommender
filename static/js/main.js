
/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/* Menu show */
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

/* Menu hidden */
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

const linkAction = () =>{
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () =>{
    const header = document.getElementById('header')
    // Add a class if the bottom offset is greater than 50 of the viewport
    this.scrollY >= 50 ? header.classList.add('bg-header') 
                       : header.classList.remove('bg-header')
}
window.addEventListener('scroll', scrollHeader)

/*=============== SHOW SCROLL UP ===============*/ 
const scrollUp = () =>{
	const scrollUp = document.getElementById('scroll-up')
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the a tag with the scrollup class
	this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
						: scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp)

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')
    
const scrollActive = () =>{
  	const scrollDown = window.scrollY

	sections.forEach(current =>{
		const sectionHeight = current.offsetHeight,
			  sectionTop = current.offsetTop - 58,
			  sectionId = current.getAttribute('id'),
			  sectionsClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']')

		if(scrollDown > sectionTop && scrollDown <= sectionTop + sectionHeight){
			sectionsClass.classList.add('active-link')
		}else{
			sectionsClass.classList.remove('active-link')
		}                                                    
	})
}
window.addEventListener('scroll', scrollActive)

/*=============== PARALLAX ===============*/
var parallax = new Rellax('.parallax');

/*=============== GSAP ANIMATION ===============*/
gsap.from('.home__village', 1.2, {opacity: 0, y:100, delay:.1})
gsap.from('.home__pine', 1.2, {opacity: 0, y:150, delay:.3})
gsap.from('.home__mountain-2', 1.2, {opacity: 0, x:150, delay:.5})
gsap.from('.home__mountain-3', 1.2, {opacity: 0, x:-150, delay:.6})
gsap.from('.home__mountain-1', 1.2, {opacity: 0, y:250, delay:.7})
gsap.from('.home__moon', 1.2, {opacity: 0, y:200, delay:.8})
gsap.from('.home__trineo', 1.2, {opacity: 0, y:200, delay:1.3})
gsap.from('.home__spider', 1.1, {opacity: 0, y:-100, delay:1.7})
gsap.from('.home__iron', 1.2, {opacity: 0, y:160, delay:1.5})
gsap.from('.home__strange', 1.3, {opacity: 0, x:-20, delay:1.9})
gsap.from('.home__captain', 1.4, {opacity: 0, x:-20, delay:1.9})
gsap.from('.home__hulk', 1.5, {opacity: 0, x:160, delay:1.5})

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2500,
    delay: 400
})

sr.reveal(`.results`, {origin: 'right'})

/* =====================Local Storage====================== */
document.addEventListener("DOMContentLoaded", function() {
    let message = document.getElementById("content");
    let lastVisit = localStorage.getItem("lastVisit");
  
    if (lastVisit) {
      message.textContent = "Welcome back! Last visited: " + lastVisit;
    } else {
      message.textContent = "Welcome!";
    }
  
    // Update last visit time
    localStorage.setItem("lastVisit", new Date().toLocaleString());
})
