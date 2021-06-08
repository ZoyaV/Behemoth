
async function fetchInterests() {
  const ints = fetch('http://localhost:5000/interests').then(res => res.json());

  return ints;
}

async function fetchSex() {
  const sexes = fetch('http://localhost:5000/sex').then(res => res.json());

  return sexes;
}

async function setPeople() {
  const sexes = await fetchSex();
  const { male, female } = sexes;
  const people = male + female;
  document.getElementById('num_of_people').innerText = people;
  document.getElementById('num_of_men').innerText = male;
  document.getElementById('num_of_women').innerText = female;
}

async function setAges() {

}

async function setInterests() {
  /**
   * @type {Array}
   */
  const { interest } = await fetchInterests();
  const container = [];
  const root = document.getElementById('interests-container');
  const VISIBILITY_RATE = 5;

  const total_num = interest.reduce(function (total, curr) {
    const { sets } = curr;
    if (typeof sets === 'string')
      return total + curr.size;
    return total;
  }, 0);

  // Отрисовываем бары
  interest.forEach((val, i, arr) => {
    const { sets } = val;

    if (typeof sets === 'string') {
      const { size } = val;
      const percentage = Math.round((size / total_num) * 100);

      const el_container = document.createElement('div');

      const header = document.createElement('h4');
      header.classList.add('small', 'font-weight-bold');
      header.innerText = sets;

      const span = document.createElement('span');
      span.classList.add('float-right');
      span.innerText = percentage + '%';

      const progress = document.createElement('div');
      progress.classList.add('progress', 'mb-4');

      const progress_inner = document.createElement('div');
      progress_inner.classList.add('progress-bar');
      progress_inner.style.backgroundColor = 'rgba(255, 30, 30,' + percentage / 100 * VISIBILITY_RATE + ')';
      progress_inner.style.width = percentage + '%';

      header.appendChild(span);
      progress.appendChild(progress_inner);
      el_container.appendChild(header);
      el_container.appendChild(progress);

      root.appendChild(el_container)
    }
  });

  interest.forEach(int => {
    if (typeof int.sets === 'string') {
      int.sets = [int.sets]
    }
  })

  return interest;
}

(async () => {
  await setPeople();
  const sets = await setInterests();
  window.sets = sets;
})();
