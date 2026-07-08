const preloadImages = [];

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".game-gif").forEach(img => {

        const gifUrl = img.dataset.gif;

        const preload = new Image();
        preload.src = gifUrl;

        preloadImages.push(preload);

        img.addEventListener("mouseenter", () => {
            img.src = gifUrl;
        });

        img.addEventListener("mouseleave", () => {
            img.src = img.dataset.still;
        });

    });

});