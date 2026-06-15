document.querySelectorAll('[data-bs-theme-value]').forEach(button => { 
        button.addEventListener('click', () => {
          const theme = button.getAttribute('data-bs-theme-value');
          document.documentElement.setAttribute('data-bs-theme', theme);
          localStorage.setItem('theme', theme);

          document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-pressed', 'false');
          });
          button.classList.add('active');
          button.setAttribute('aria-pressed', 'true');
        });
      });

      document.addEventListener('DOMContentLoaded', () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
          document.documentElement.setAttribute('data-bs-theme', savedTheme);
          const activeButton = document.querySelector(`[data-bs-theme-value="${savedTheme}"]`);

          if (activeButton){
            activeButton.classList.add('active');
            activeButton.setAttribute('aria-pressed', 'true');
          }
        }
      });