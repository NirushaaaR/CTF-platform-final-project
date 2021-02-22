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
      console.log(data);
      if (data.correct) {
        location.reload();
      }
    }
  });
});