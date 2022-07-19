document.addEventListener('DOMContentLoaded', function () {
    toggler = document.getElementsByClassName('navbar-toggler')[0]
	toggler.addEventListener('click', function () {
		subnav = document.getElementById('navbarColor01')
		subnav.style.transition = "2s"
		if (subnav.style.display == "none") {
			subnav.style.display = "block"
		}
		else
			subnav.style.display = "none"
	});
});