const script = document.createElement("script");
script.type = "text/javascript";
script.src =
  "https://cdn.tiny.cloud/1/8iuxongsnjxs7gyus3crja2c0nel6q86b3m820incum0jmpv/tinymce/5/tinymce.min.js";
script.referrerPolicy = "origin";
// append tinymce in head tag
document.head.appendChild(script);

script.onload = function () {
  tinymce.init({
    // selector: ".tinymce-editor",
    selector: "textarea",
    height: 500,
    plugins: 'code advlist link image lists media tinydrive imagetools',
    toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent',
    tinydrive_token_provider: '/jwt'
  });
};
