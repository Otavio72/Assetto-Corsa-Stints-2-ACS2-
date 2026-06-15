        const emailInput = document.getElementById("email");
        const mensagemEmail = document.getElementById("mensagem-email");
        const requisitoEmail = [{regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, msg: "Email invalido"}];

        emailInput.addEventListener("input", () => {
          const email = emailInput.value;

          let erros = [];

          requisitoEmail.forEach(regra => {
            if (!regra.regex.test(email)) {
              erros.push(regra.msg);
            }

            if (erros.length === 0){
                mensagemEmail.innerText = "✅ Email válido!"
                mensagemEmail.style.color = "green"
            } else {
                mensagemEmail.innerText = "❌ Email invalido!"
                mensagemEmail.style.color = "red"
            }

          });

        }); 

        const senhaInput = document.getElementById("senha");
        const mensagem = document.getElementById("mensagem");

        const requisitos = [
            { regex: /.{8,}/, msg: "Mínimo 8 caracteres" },
            { regex: /[A-Z]/, msg: "Pelo menos uma letra maiúscula" },
            { regex: /[a-z]/, msg: "Pelo menos uma letra minúscula" },
            { regex: /[0-9]/, msg: "Pelo menos um número" },
            { regex: /[^A-Za-z0-9]/, msg: "Pelo menos um caractere especial" }
        ];

            senhaInput.addEventListener("input", () => {
            const senha = senhaInput.value;
            let senhaValida = true;
            
            requisitos.forEach((regra, index) => {
              const valido = regra.regex.test(senha);
              const item = document.getElementById(`req${index}`);
              item.textContent = `${valido ? "✅": "❌"} ${regra.msg}`;
              item.style.color = valido ? "green" : "red";

              if (!valido) senhaValida = false;

            });

            if (senhaValida) {
              mensagem.textContent = "✅ Senha válida!";
              mensagem.style.color = "green"
            } else {
                  mensagem.textContent = "❌ Senha inválida";
                  mensagem.style.color = "red";
            } 

        });