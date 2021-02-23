function adjustActivePage(from, to) {
  $(`.menu-page[data-slide-to='${from}']`).removeClass("active");
  $(`.menu-page[data-slide-to='${to}']`).addClass("active");
}

$(".menu-page").each((index, elem) => {
  elem.onclick = e => {
    $('.carousel').carousel(index);
  };
});

$('#myCarousel').on('slide.bs.carousel', function (e) {
  adjustActivePage(e.from, e.to);
})


$(".task-form").submit(function (e) {
  e.preventDefault();

  const form = $(this);
  const url = form.attr('action');
  const task_id = $('input[name="task_id"]', form).val();

  $.ajax({
    type: "POST",
    url: url,
    data: form.serialize(),
    success: function (data) {
      alert(data.message);
      if (data.correct) {
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
        if (taskConclusion) taskConclusion.innerHTML = data.conclusion;
      }
    }
  });
});