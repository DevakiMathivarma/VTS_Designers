document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll(".card h2");
    const animateCounter = (counter) => {
        const target = +counter.innerText;
        counter.innerText = "0";
        const updateCount = () => {
            const current = +counter.innerText;
            const increment = Math.ceil(target / 50);
            if (current < target) {
                counter.innerText = Math.min(current + increment, target);
                setTimeout(updateCount, 30);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target); // run once
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
});
document.addEventListener("DOMContentLoaded", function () {
    const chooseBtn = document.getElementById('choose-files');
    const fileInput = document.getElementById('file-input');

    if (chooseBtn && fileInput) {
        chooseBtn.addEventListener('click', function () {
            fileInput.click(); // Trigger file selection
        });
    }
});