      document.addEventListener('DOMContentLoaded', () => {
        const cartButton = document.getElementById("btnCarrinho");
        const trigger = document.querySelector('[data-bs-target="#modalCarrinho"]')

        if (trigger) {
          trigger.addEventListener('click', function () {
            const url = this.dataset.url;
            fetch(url)
              .then(response => response.text())
              .then(html => {
                document.getElementById('modalCarrinhoContent').innerHTML = html;
              });
          });
        }
      });

      function atualizarCarrinho() {
        fetch('/modal_carrinho/')
        .then(response => response.text())
        .then(html => {
          document.getElementById('conteudoCarrinho').innerHTML = html;
        });
    }