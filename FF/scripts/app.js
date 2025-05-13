document.addEventListener('DOMContentLoaded', () => {
    // Código para inicializar a interatividade do site
    console.log('O site está pronto para interatividade!');
    
    document.getElementById('actionButton').addEventListener('click', () => {
        alert('Botão clicado!');
    });
});
         function showWelcomeMessage() {
            alert("Bem-vindo ao Lobby!");
        }
    // Exemplo de animação com CSS
    const welcomeMessage = document.getElementById('welcomeMessage');
        const buttons = document.querySelectorAll('.button');
        buttons.forEach(button => {
            button.addEventListener('mouseover', () => {
                button.style.transform = 'scale(1.1)';
            });
            button.addEventListener('mouseout', () => {
                button.style.transform = 'scale(1)';
            });
        })