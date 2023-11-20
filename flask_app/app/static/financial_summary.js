// Função para verificar quantos dias tem o mes atual
function _numDias(){
  var objData = new Date(),
      numAno = objData.getFullYear(),
      numMes = objData.getMonth()+1,
      numDias = new Date(numAno, numMes, 0).getDate();

  return numDias;
}


// Função para preencher a tabela com os dados recebidos
  function preencherSpanBoardItens(data) {
    // Obtém a referência da tabela no HTML
    const span_realized_expenses = document.getElementById("span_realized_expenses");
    const span_planned_expenses = document.getElementById("span_planned_expenses");
    const span_realized_income = document.getElementById("span_realized_income");
    const span_planned_income = document.getElementById("span_planned_income");
    const span_realized_balance = document.getElementById("span_realized_balance");

    const span_max_expense_day = document.getElementById("span_max_expense_day");

    const svg_container_renda_input_hidden = document.getElementById("svg_container_renda_input_hidden");
    const svg_container_despesa_input_hidden = document.getElementById("svg_container_despesa_input_hidden");
    
    
     // Verifica se os spans existem e se há dados no array recebido
    if (data.length > 0) {
      // Preenche os spans com os valores do primeiro objeto do array (nesse caso, assumindo que há apenas um objeto no array)
      span_realized_expenses.textContent = "R$ "+data[0].realized_expenses.toFixed(2);
      span_planned_expenses.textContent = "R$ "+data[0].planned_expenses.toFixed(2);
      span_realized_income.textContent   = "R$ "+data[0].realized_income.toFixed(2);
      span_planned_income.textContent   = "R$ "+data[0].planned_income.toFixed(2);
      span_realized_balance.textContent = "R$ "+data[0].realized_balance.toFixed(2);
      span_planned_income.textContent   = "R$ "+data[0].planned_income.toFixed(2);
      span_realized_balance.textContent = "R$ "+data[0].realized_balance.toFixed(2);
          
      
      //calcular o valor máximo disponível para gasto médio diário
      span_max_expense_day.textContent = "R$ "+parseFloat(data[0].realized_balance / _numDias()).toFixed(2);

      //preenche os campos ocultos para permitir o desenho dos gráficos
      svg_container_renda_input_hidden.value = data[0].income_percentage.toFixed(2);
      svg_container_despesa_input_hidden.value = data[0].expense_percentage.toFixed(2);
    }
    
  }
  
  // Função para fazer a requisição HTTP e chamar a função de preencher a tabela
  function fetchDataAndPopulateSpanBoards() {
    // URL da API
    const apiUrl = '/transactions/financial_summary';
  
    // Faz a requisição HTTP
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        // Chama a função para preencher a os items com os dados recebidos
        preencherSpanBoardItens(data);
      })
      .catch(error => {
        console.error('Ocorreu um erro ao buscar os dados:', error);
      });
  }
  
  // Chama a função para buscar os dados e preencher a tabela quando a página carregar
  window.addEventListener('load', fetchDataAndPopulateSpanBoards);
  
  