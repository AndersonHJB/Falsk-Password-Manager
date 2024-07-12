document.addEventListener('DOMContentLoaded', function () {
    var clipboard = new ClipboardJS('.copy-btn');

    clipboard.on('success', function (e) {
        var button = e.trigger;
        button.classList.add('copied');

        setTimeout(function () {
            button.classList.remove('copied');
        }, 2000);
    });
});