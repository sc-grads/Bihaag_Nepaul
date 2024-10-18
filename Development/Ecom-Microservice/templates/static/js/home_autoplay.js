document.addEventListener('DOMContentLoaded', function() {
    var video = document.getElementById('background-video');

    // Play video
    video.play().catch(function(error) {
        console.log("Autoplay was prevented: ", error);

        // Optional: Add a play button if autoplay fails
        var playButton = document.createElement('button');
        playButton.textContent = 'Play';
        playButton.onclick = function() {
            video.play();
            this.style.display = 'none';
        };
        video.parentNode.insertBefore(playButton, video.nextSibling);
    });

    // Optional: Pause video when not visible to save resources
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            video.pause();
        } else {
            video.play().catch(function(error) {
                console.log("Playback was prevented: ", error);
            });
        }
    });
});




document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('menu-btn');
    const navMenu = document.getElementById('nav-menu');
    const closeBtn = document.getElementById('close-nav');
    const overlay = document.getElementById('overlay');

    menuBtn.addEventListener('click', function(e) {
        e.preventDefault();
        navMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    closeBtn.addEventListener('click', function() {
        navMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    });

    overlay.addEventListener('click', function() {
        navMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    });
});