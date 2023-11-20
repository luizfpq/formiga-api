// Função para gerar a imagem SVG com base no percentual fornecido
function gerarSVG_despesa(percentual) {
    const svgNS = 'http://www.w3.org/2000/svg';
    const svgWidth = 200;
    const svgHeight = 145;
  
    // Cria o elemento SVG
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('width', svgWidth);
    svg.setAttribute('height', svgHeight);
    svg.setAttribute('xmlns', svgNS);
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Medidor de Porcentagem');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    svg.setAttribute('focusable', 'false');
  
    // Cria o retângulo base preto
    const baseRect = document.createElementNS(svgNS, 'rect');
    baseRect.setAttribute('width', '100%');
    baseRect.setAttribute('height', '100%');
    baseRect.setAttribute('fill', '#664d03');
    svg.appendChild(baseRect);
  
    // Calcula a altura do retângulo de preenchimento com base no percentual
    const filledHeight = (percentual / 100) * svgHeight;
  
    // Cria o retângulo preenchido com a cor desejada
    const filledRect = document.createElementNS(svgNS, 'rect');
    filledRect.setAttribute('width', '100%');
    filledRect.setAttribute('height', filledHeight);
    filledRect.setAttribute('fill', '#b2a681');
    svg.appendChild(filledRect);
  
    // Cria o texto exibindo a porcentagem
    const text = document.createElementNS(svgNS, 'text');
    text.setAttribute('x', '50%');
    text.setAttribute('y', '50%');
    text.setAttribute('fill', '#fff');
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('dy', '.3em');
    text.textContent = `${percentual}%`;
    svg.appendChild(text);
  
    return svg;
  }

  // Obtém o elemento onde deseja exibir a imagem SVG
  const svgContainerDespesa = document.getElementById('svg-container-despesa');
  
  // Define o percentual que você deseja exibir (exemplo: 75%)
  const percentualDespesa = document.getElementById('svg_container_despesa_input_hidden').value;
  
  // Gera a imagem SVG com o percentual desejado
  const svgElementDespesa = gerarSVG_despesa(percentualDespesa);
  
  // Adiciona a imagem SVG ao elemento container na página
  svgContainerDespesa.appendChild(svgElementDespesa);