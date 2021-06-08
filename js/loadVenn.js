document.addEventListener('setsReady', (e) => {
  setTimeout(() => {
    var chart = venn.VennDiagram();
    const { sets } = e.detail;
    d3.select("#venn").datum(sets).call(chart);
  }, 1000);
});