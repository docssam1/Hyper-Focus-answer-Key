(function () {
  var base = (document.currentScript && document.currentScript.src)
    ? document.currentScript.src.replace(/[^\/]+$/, '')
    : './data/';
  function loadSync(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    xhr.send(null);
    if (xhr.status === 200) { new Function(xhr.responseText)(); }
  }
  loadSync(base + 'sq-a.js');
  loadSync(base + 'sq-b.js');
  loadSync(base + 'sq-c.js');
  window.GFIELD_SIMILAR_QUESTIONS = [].concat(
    window.GFIELD_SQ_A || [],
    window.GFIELD_SQ_B || [],
    window.GFIELD_SQ_C || []
  );
})();
