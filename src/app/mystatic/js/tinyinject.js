const script = document.createElement("script");
script.type = "text/javascript";
script.src =
  "https://cdn.tiny.cloud/1/8iuxongsnjxs7gyus3crja2c0nel6q86b3m820incum0jmpv/tinymce/5/tinymce.min.js";
// append tinymce in head tag
document.head.appendChild(script);

script.onload = function () {
  tinymce.init({
    selector: "#id_description",
    height: 656,
  });
};
