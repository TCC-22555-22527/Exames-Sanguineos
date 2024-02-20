document.getElementById('combined-search-button').addEventListener('click', function () {
    const searchInput = document.querySelector('#search-box');
    const dateInput = document.querySelector('#search_date');
    const searchForm = document.querySelector('.search-form');
    const dateSearchForm = document.querySelector('.date-search-form');

    // Verifique se ambos os campos estão preenchidos corretamente
    const searchValid = searchInput.value.trim().length > 0;
    const dateValid = dateInput.value.trim().length > 0;

    if (searchValid || dateValid) {
        // Se algum dos campos estiver preenchido corretamente, envie os formulários
        if (searchValid) searchForm.submit();
        if (dateValid) dateSearchForm.submit();
    } 
});

// Desabilitar campo de data se estiver vazio
document.getElementById('combined-search-button').addEventListener('click', function () {
    const dateInput = document.querySelector('#search_date');
    if (dateInput.value.trim().length === 0) {
        dateInput.disabled = true;
    }
});