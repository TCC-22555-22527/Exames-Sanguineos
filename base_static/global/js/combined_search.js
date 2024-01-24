document.getElementById('combined-search-button').addEventListener('click', function () {
    const searchInput = document.querySelector('.search-input');
    const dateInput = document.querySelector('#search_date');
    const searchForm = document.querySelector('.search-form');
    const dateSearchForm = document.querySelector('.date-search-form');

    // Verifique se o campo de pesquisa ou o campo de data estão preenchidos
    if (searchInput.value || dateInput.value) {
        // Se algum dos campos estiver preenchido, envie os formulários
        searchForm.submit();
        dateSearchForm.submit();
    }
});