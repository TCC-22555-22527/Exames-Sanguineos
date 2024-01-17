document.querySelector('.main-form').addEventListener('submit', function (event) {
    // Previne o comportamento padrão do formulário para evitar o envio antes do processamento
    event.preventDefault();

    // Verifica se o formulário é válido
    if (event.target.checkValidity()) {
        // Mostra o overlay de loading
        document.getElementById('loading-overlay').style.display = 'flex';

        // Após mostrar o overlay, você pode permitir o envio do formulário manualmente
        // Se desejar, pode adicionar um código aqui para enviar o formulário com AJAX, por exemplo
        // document.querySelector('.main-form').submit();
    } else {    
        // Se o formulário não for válido, exibe mensagens de erro
        alert("Por favor, preencha todos os campos corretamente.");
    }
});