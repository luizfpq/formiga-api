  // Função para preencher a tabela com os dados recebidos
  function preencherTabela(data) {
    // Obtém a referência da tabela no HTML
    const table = document.querySelector('.table');
  
    // Cria o cabeçalho da tabela
    const thead = table.createTHead();
    const headerRow = thead.insertRow();
    const headers = ['Categoria', 'Valor'];
  
    // Preenche o cabeçalho da tabela
    headers.forEach(headerText => {
      const th = document.createElement('th');
      const text = document.createTextNode(headerText);
      th.appendChild(text);
      headerRow.appendChild(th);
    });
  
    // Preenche os dados na tabela
    const tbody = table.createTBody();
    data.forEach(item => {
      if (item.total_value != 0) {
        const row = tbody.insertRow();
  
        const nameCell = row.insertCell();
        nameCell.textContent = item.category_name;
    
        const valueCell = row.insertCell();
        valueCell.textContent = item.total_value;
      }
    });
  }
  
  // Função para fazer a requisição HTTP e chamar a função de preencher a tabela
  function fetchDataAndPopulateTable() {
    // URL da API
    const apiUrl = '/transactions/expense_category_totals';
  
    // Faz a requisição HTTP
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        // Chama a função para preencher a tabela com os dados recebidos
        preencherTabela(data);
      })
      .catch(error => {
        console.error('Ocorreu um erro ao buscar os dados:', error);
      });
  }
  
  // Chama a função para buscar os dados e preencher a tabela quando a página carregar
  window.addEventListener('load', fetchDataAndPopulateTable);
