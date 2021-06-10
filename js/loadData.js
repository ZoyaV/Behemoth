
async function fetchInterests(index) {
  const ints = fetch('http://localhost:5000/interests?' + 'complex=' + index).then(res => res.json());

  return ints;
}

async function fetchSex(index) {
  const sexes = fetch('http://localhost:5000/sex?' + 'complex=' + index).then(res => res.json());

  return sexes;
}

async function setPeople(index) {
  const sexes = await fetchSex(index);
  const { male, female } = sexes;
  const people = male + female;
  document.getElementById('num_of_people').innerText = people;
  document.getElementById('num_of_men').innerText = male;
  document.getElementById('num_of_women').innerText = female;
}

async function setInterests(index) {
  /**
   * @type {Array}
   */
  const { interest } = await fetchInterests(index);

  const root = document.getElementById('interests-container');
  const children = Array.from(root.children);
  const VISIBILITY_RATE = 5;

  const total_num = interest.reduce(function (total, curr) {
    const { sets } = curr;
    if (sets.length === 1)
      return total + curr.size;
    return total;
  }, 0);

  if (children.length == 0) {
    const container = [];

    // Отрисовываем бары
    interest.forEach((val, i, arr) => {
      const { sets } = val;
      console.log(sets);
      if (sets.length === 1) {
        const { size } = val;
        const percentage = Math.round((size / total_num) * 100);

        const el_container = document.createElement('div');

        const header = document.createElement('h4');
        header.classList.add('small', 'font-weight-bold');

        header.innerText = sets[0].replace('hobbi', '').toUpperCase();

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
        container.push(el_container);
      }
    });

    root.append(...container);
  } else {
    for (let i = 0; i < children.length; i++) {
      const { size } = interest[i];
      const percentage = Math.round((size / total_num) * 100);
      const progress = Array.from(children[i].children).filter(ch => Object.values(ch.classList).indexOf('progress') != -1)[0];
      const progressBar = progress.children[0];
      progressBar.style.width = percentage + '%';
      progressBar.style.backgroundColor = 'rgba(255, 30, 30,' + percentage / 100 * VISIBILITY_RATE + ')';
    }

  }



  interest.forEach(int => {
    if (typeof int.sets === 'string') {
      int.sets = [int.sets]
    }
  })

  return interest;
}




async function loadPeople(index = 0) {
  await setPeople(index);
  const sets = await setInterests(index);
  // window.sets = sets;

  const setsReady = new CustomEvent('setsReady', {
    detail: {
      sets: sets
    },
    bubbles: true
  });

  document.dispatchEvent(setsReady);
};



loadPeople();