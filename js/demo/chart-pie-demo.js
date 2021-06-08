// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


async function fetchAges(index = 0) {
  const ages = await fetch('http://localhost:5000/ages?' + 'complex=' + index).then(res => res.json());

  return ages;
}

async function loadAge(index = 0) {
  // Pie Chart with Ages
  const ages = await fetchAges(index);
  const labels = Object.keys(ages);
  const data = Object.values(ages);

  const ages_container = document.getElementById('age_labels');
  const children = Array.from(ages_container.children);
  children.forEach(ch => ages_container.removeChild(ch));

  const backgroundColors = ['#FB4B4B', '#FFD355', '#91FF60', '#ADF2FF', '#B088FF'];
  const hoverColors = ['#FE3131', '#FFC726', '#60FF19', '#5EE5FE', '#8142FF'];

  labels.forEach((l, index) => {
    const span = document.createElement('span');
    span.classList.add('mr-2');

    const i = document.createElement('i');
    const strong = document.createElement('strong');
    strong.innerText = l.toUpperCase();

    i.classList.add('fas', 'fa-circle', 'mr-1');
    i.style.color = backgroundColors[index];
    span.appendChild(i);
    span.appendChild(strong);
    ages_container.appendChild(span);
  })


  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: backgroundColors,
        hoverBackgroundColor: hoverColors,
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
  });

};


document.addEventListener('loadData', (e) => {
  loadAge(e.detail.index);
})

loadAge();

