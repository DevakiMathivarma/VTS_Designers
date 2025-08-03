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
    const fileListContainer = document.getElementById('file-list'); // Container to show file names
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']; // Allowed image types

    if (chooseBtn && fileInput) {
        chooseBtn.addEventListener('click', function () {
            fileInput.click(); // Trigger file selection
        });

        fileInput.addEventListener('change', function () {
            fileListContainer.innerHTML = ''; // Clear previous list
            let validFiles = [];

            if (fileInput.files.length > 0) {
                for (let i = 0; i < fileInput.files.length; i++) {
                    if (!allowedTypes.includes(fileInput.files[i].type)) {
                        alert(`"${fileInput.files[i].name}" is not an image. Only .jpg, .jpeg, .png, .webp files are allowed.`);
                        continue;
                    }
                    validFiles.push(fileInput.files[i]);
                }

                if (validFiles.length > 0) {
                    validFiles.forEach(file => {
                        const fileName = document.createElement('p');
                        fileName.textContent = file.name;
                        fileName.style.fontSize = "14px";
                        fileName.style.margin = "4px 0";
                        fileListContainer.appendChild(fileName);
                    });
                } else {
                    fileInput.value = ''; // Reset if no valid files
                }
            }
        });
    }
});
