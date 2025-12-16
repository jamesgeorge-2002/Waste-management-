document.addEventListener('DOMContentLoaded', function () {
  const localBodySelects = document.querySelectorAll('select[name="local_body"]');

  localBodySelects.forEach(function (select) {
    select.addEventListener('change', function (e) {
      const lb = e.target.value;
      const form = e.target.closest('form');
      const wardSelect = form.querySelector('select[name="ward"]');
      if (!wardSelect) return;
      fetch(`/locations/api/wards/?local_body=${lb}`)
        .then(res => res.json())
        .then(data => {
          wardSelect.innerHTML = '';
          if (data.wards && data.wards.length) {
            data.wards.forEach(w => {
              const opt = document.createElement('option');
              opt.value = w.id;
              opt.textContent = `Ward ${w.number} - ${w.name}`;
              wardSelect.appendChild(opt);
            });
          } else {
            const opt = document.createElement('option');
            opt.textContent = 'No wards available';
            wardSelect.appendChild(opt);
          }
        })
        .catch(err => console.error(err));
    });
  });
});
