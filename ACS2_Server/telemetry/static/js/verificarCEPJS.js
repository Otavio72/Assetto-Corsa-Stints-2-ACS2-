      document.getElementById("zip").addEventListener("blur", function(){
        
        const zip = this.value.replace(/\D/g, "");

        if (zip.length !== 8) return;

        fetch(`https://viacep.com.br/ws/${zip}/json/`)
        .then((response) => response.json())
        .then((data) => {
          if (data.erro){
            alert("CEP não encontrado");
            return;
          }

          document.getElementById("address").value = data.logradouro;
          document.getElementById("state").value = data.uf;
          document.getElementById("bairro").value = data.bairro;
          document.getElementById("cidade").value = data.localidade;
        })
        .catch(() => alert("Erro ao buscar o CEP"));
      });