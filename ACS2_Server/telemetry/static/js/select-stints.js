let selected = [];

document.querySelectorAll(".select-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
        e.preventDefault();

        const card = btn.closest(".stint-card");
        const id = card.dataset.id;

        // se já está selecionado → remove
        if (selected.includes(id)) {
            selected = selected.filter(i => i !== id);
            card.classList.remove("selected");
        } 
        else {
            // máximo 2
            if (selected.length < 2) {
                selected.push(id);
                card.classList.add("selected");
            }
        }

        console.log(selected);

        updateCompareButton();
    });
});

function updateCompareButton() {
    const btn = document.getElementById("compareBtn");
    const game = document.getElementById("page-data").dataset.game;

    if (!btn) return;

    if (selected.length === 2) {
        btn.style.display = "block";

        btn.href = `/analise/${game}/${selected[0]}/${selected[1]}/`;
    } 
    else {
        btn.style.display = "none";
    }
    
}

console.log("selected:", selected);

document.getElementById("compareBtn").addEventListener("click", (e) => {
    e.preventDefault();

    if (selected.length !== 2) return;

    const overlay = document.getElementById("loading-overlay");
    overlay.classList.remove("hidden");

    const game = document.getElementById("page-data").dataset.game;

    const url = `/analise/${game}/${selected[0]}/${selected[1]}/`;

    // pequeno delay pra UX (opcional mas bonito)
    setTimeout(() => {
        window.location.href = url;
    }, 400);
});