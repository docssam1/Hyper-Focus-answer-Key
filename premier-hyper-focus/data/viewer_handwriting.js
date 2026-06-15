// premier-hyper-focus/data/viewer_handwriting.js

/**
 * GFIELD HF Handwriting Player
 * -----------------------------
 * handwritingData 객체를 사용하여 SVG 손글씨 애니메이션을 재생합니다.
 * 
 * 필요 라이브러리:
 * - Vivus.js (for SVG path animation)
 * - Khoshnus.js (for handwriting-style text animation)
 * 
 * HTML 구조 요구사항:
 * - <svg id="handwriting-svg"><path id="handwriting-path"/></svg>
 * - <div id="math-handwriting-svg"></div> (Khoshnus용)
 */

function playHandwriting(handwritingData) {
  const svgElement = document.getElementById('handwriting-svg');
  const pathElement = document.getElementById('handwriting-path');

  if (!svgElement || !pathElement || !handwritingData || !handwritingData.svgPath) {
    console.error("Handwriting SVG elements or data are missing.");
    return;
  }

  if (svgElement.vivus) {
    svgElement.vivus.reset().destroy();
  }
  
  pathElement.setAttribute('d', handwritingData.svgPath);
  pathElement.setAttribute('stroke', handwritingData.color || '#FF0000');
  pathElement.setAttribute('stroke-width', '2');
  pathElement.style.transition = 'stroke 0.3s, stroke-width 0.3s';

  if (handwritingData.emphasisTrigger === 'CALCULATION_ERROR') {
    pathElement.setAttribute('stroke-width', '4');
    pathElement.setAttribute('stroke', '#E53935');
  } else {
    pathElement.setAttribute('stroke-width', '2.5');
    pathElement.setAttribute('stroke', handwritingData.color || '#007BFF');
  }

  svgElement.vivus = new Vivus('handwriting-svg', {
    duration: handwritingData.duration || 2000,
    type: 'delayed',
    pathTimingFunction: Vivus.EASE_OUT,
    start: 'autostart'
  }, (vivusInstance) => {
    if (handwritingData.emphasisTrigger === 'CALCULATION_ERROR') {
      pathElement.classList.add('pulsate-emphasis');
    }
  });
}

function playMathHandwriting(formulaText, targetElementId = 'math-handwriting-svg') {
  const targetElement = document.getElementById(targetElementId);
  if (!targetElement) {
    console.error(`Target element for math handwriting #${targetElementId} not found.`);
    return;
  }
  if (typeof Khoshnus === 'undefined') {
    console.error("Khoshnus.js library is not loaded.");
    return;
  }
  
  targetElement.innerHTML = '';

  const instance = new Khoshnus(targetElement, {
    font: 'Parisienne',
    color: '#333333',
    size: '48px',
    padding: 10
  });

  instance.write(formulaText, {
    writeConfiguration: {
      eachLetterDelay: 150,
      strokeDelay: 50,
    }
  });
}
