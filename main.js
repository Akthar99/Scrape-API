

var menu = document.querySelector('.head-navbar');
var menu_style = document.querySelector('.head-navbar-style');

function MenuBar(x) {
	// play the animation when user click
	console.log("menu button clicked");
	x.classList.toggle('change');
	if (menu.classList.contains('active')) {
		menu.style.display = 'none';
	} else {
		menu.style.display = 'flex';
	}
	if (menu_style.classList.contains('active')) {
		menu_style.style.height = '40px';
	} else {
		menu_style.style.height = '400px';
	}
	menu.classList.toggle('active');
	menu_style.classList.toggle('active');
}


function checkWindowSize() {
	if (window.innerWidth < 600) {
		return 1;
	} else {
		return 0;
	}
}

window.addEventListener('resize', function() {
	if (checkWindowSize() == 1) {
		menu.style.display = 'none';
	} else if (checkWindowSize() == 0) {
		menu.style.display = 'flex';
	}
})




const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        } else {
            entry.target.classList.remove("show");
        }
    })
})

const hiddenElements = document.querySelectorAll(".hidden");
hiddenElements.forEach((element) => observer.observe(element));
