document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".game-video").forEach(video => {

        const card = video.closest(".car-wrap");

        card.addEventListener("mouseenter", () => {
            video.play();
        });

        card.addEventListener("mouseleave", () => {
            video.pause();
            video.currentTime = 0;
        });

    });

});