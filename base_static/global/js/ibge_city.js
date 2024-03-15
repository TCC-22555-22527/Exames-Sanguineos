document.addEventListener("DOMContentLoaded", function() {
    // Função para carregar cidades com base no estado selecionado
    function carregarCidades() {
        var estadoSelecionado = document.getElementById('id_state').value;
        var selectCidade = document.getElementById('id_city');

        // Limpa as opções de cidades anteriores
        selectCidade.innerHTML = '<option value="">Selecione a cidade</option>';

        if (estadoSelecionado) {
            fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoSelecionado}/municipios`)
            .then(response => response.json())
            .then(data => {
                data.forEach(cidade => {
                    var option = document.createElement('option');
                    option.value = cidade.nome;
                    option.textContent = cidade.nome;
                    selectCidade.appendChild(option);
                });
            })
            .catch(error => console.error('Erro ao carregar cidades:', error));
        }
    }

    // Adiciona um listener para o evento de mudança no campo de estado
    document.getElementById('id_state').addEventListener('change', carregarCidades);

    // Carrega as cidades quando a página é carregada
    carregarCidades();
});
