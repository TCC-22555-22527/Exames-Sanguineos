
    const stateSelect = document.querySelector('#id_state');
    const citySelect = document.querySelector('#id_city');
    stateSelect.addEventListener('change', async () => {
        const response = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${stateSelect.value}/municipios`);
        const cities = await response.json();

        citySelect.innerHTML = '';
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city.nome;
            option.text = city.nome;
            citySelect.appendChild(option);
        });
    });

