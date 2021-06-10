const nodes = document.getElementById('microdistricts');
const districts = Array.from(nodes.children);

districts.forEach(d => {
  d.addEventListener('click', (e) => {
    const dIndex = districts.indexOf(d);
    const loadDataEvent = new CustomEvent('loadData', {
      detail: {
        index: dIndex
      },
      bubbles: true
    });

    d.dispatchEvent(loadDataEvent);
  })
})
