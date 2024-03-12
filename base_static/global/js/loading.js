document.addEventListener('DOMContentLoaded', function () {
    // Adicionar ouvinte de evento para o envio do formulário
    var form = document.getElementById('form-send-mic');
    form.addEventListener('submit', function (event) {
        // Verificar se o formulário é válido antes de mostrar o overlay de loading
        if (form.checkValidity()) {
            var loadingOverlay = document.getElementById('loading-overlay');
            loadingOverlay.style.display = 'flex';
        } else {
            // Se o formulário não for válido, impedir o envio padrão
            event.preventDefault();
        }
    });
});