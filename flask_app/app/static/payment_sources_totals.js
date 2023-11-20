// Função para preencher a div com os dados recebidos
function preencherDivSourceTotals(data) {
  // Obtém a referência da div no HTML onde deseja adicionar os elementos
  const div = document.getElementById("div_payment_sources_totals");

  // Itera sobre o array de objetos
  data.forEach(item => {
    if (item.total_value != 0) {
      // Cria um elemento 'small'
      const smallElement = document.createElement('small');
      smallElement.classList.add('text-body-secondary');
      
      // Define o conteúdo do 'small' com base nos dados do objeto atual
      smallElement.textContent = `${item.source_name}: R$ ${item.total_value.toFixed(2)}`;
      
      // Cria uma quebra de linha
      const br = document.createElement('br');
      
      // Adiciona o elemento 'small' e a quebra de linha à div
      div.appendChild(smallElement);
      div.appendChild(br);
    }
  });
}

// Função para fazer a requisição HTTP e chamar a função de preencher a div
function fetchDataAndPopulateDivSourceTotals() {
  // URL da API
  const apiUrl = '/transactions/payment_sources_totals';

  // Faz a requisição HTTP
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      // Chama a função para preencher a div com os dados recebidos
      preencherDivSourceTotals(data);
    })
    .catch(error => {
      console.error('Ocorreu um erro ao buscar os dados:', error);
    });
}

// Chama a função para buscar os dados e preencher a div quando a página carregar
window.addEventListener('load', fetchDataAndPopulateDivSourceTotals);
