document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    var chart = venn.VennDiagram();
    const sets = window.sets;
    d3.select("#venn").datum(sets).call(chart);
  }, 1000);
});