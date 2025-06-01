// Custom JavaScript for Flask Application

document.addEventListener("DOMContentLoaded", function () {
	console.log("Flask application loaded successfully!");

	// Add smooth scrolling for anchor links
	const links = document.querySelectorAll('a[href^="#"]');
	links.forEach((link) => {
		link.addEventListener("click", function (e) {
			e.preventDefault();
			const target = document.querySelector(this.getAttribute("href"));
			if (target) {
				target.scrollIntoView({
					behavior: "smooth",
				});
			}
		});
	});

	// Add active class to current navigation item
	const currentLocation = location.pathname;
	const navLinks = document.querySelectorAll(".nav-link");

	navLinks.forEach((link) => {
		if (link.getAttribute("href") === currentLocation) {
			link.classList.add("active");
		}
	});
});

// Example function for future use
function showAlert(message, type = "info") {
	const alertDiv = document.createElement("div");
	alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
	alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

	const container = document.querySelector(".container");
	container.insertBefore(alertDiv, container.firstChild);

	// Auto-dismiss after 5 seconds
	setTimeout(() => {
		alertDiv.remove();
	}, 5000);
}
