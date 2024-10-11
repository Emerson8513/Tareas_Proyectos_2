document.addEventListener('DOMContentLoaded', function () {
    const infoBox = document.querySelector('.info-box');
    const section1 = document.getElementById('section1');

    function checkVisibility() {
        const section1Rect = section1.getBoundingClientRect();
        if (section1Rect.top < window.innerHeight && section1Rect.bottom >= 0) {
            section1.querySelector('.section-content').classList.add('show-info');
        }
    }

    window.addEventListener('scroll', checkVisibility);
    checkVisibility(); // Check visibility on page load
});

