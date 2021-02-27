const tracker_url = JSON.parse(document.getElementById('tracker-url').textContent);

function adjustActivePage(from, to) {
  $(`.menu-page[data-slide-to='${from}']`).removeClass("active");
  $(`.menu-page[data-slide-to='${to}']`).addClass("active");
  // can't use ajax cause it show use fetch instead...
  fetch(tracker_url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: new URLSearchParams(`page_index=${to}`),
  });
}

$(".menu-page").each((index, elem) => {
  elem.onclick = e => {
    $('.carousel').carousel(index);
  };
});

$('#myCarousel').on('slide.bs.carousel', e => {
  adjustActivePage(e.from, e.to);
})

function showConslusion(task_id, conclusion) {
  // find element id task{id}
  const taskElement = document.getElementById(`task${task_id}`);
  // take blur out
  const blur = taskElement.querySelector(".blur");
  if (blur) blur.classList.remove("blur");
  // remove hidden wrap
  const hiddenWrap = taskElement.querySelector(".hidden-wrap");
  if (hiddenWrap) hiddenWrap.remove();
  // add conclusion to text
  const taskConclusion = taskElement.querySelector(`#taskConclusion${task_id}`);
  if (taskConclusion) taskConclusion.innerHTML = conclusion;
}

function sendFormRequest(form) {
  const url = form.attr('action');
  const task_id = $('input[name="task_id"]', form).val();
  $.ajax({
    type: "POST",
    url: url,
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    data: form.serialize(),
    success: data => {
      alert(data.message);
      if (data.correct) {
        showConslusion(task_id, data.conclusion);
      }
    }
  });
}

$(".task-form").submit(e => {
  e.preventDefault();
  const form = $(`#${e.target.id}`);
  sendFormRequest(form);
});

$(".unlock-form").submit(e => {
  e.preventDefault();
  const form = $(`#${e.target.id}`);
  sendFormRequest(form);
  document.getElementById(e.target.id).parentNode.querySelector("[data-dismiss='modal']").click()
});