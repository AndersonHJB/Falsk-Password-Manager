你好，我是悦创。

将 JavaScript 代码分离到一个单独的文件中可以使 HTML 页面更加整洁，并且有助于管理和维护代码。

以下是将时间计算功能移动到独立的 JavaScript 文件的步骤：

### 1. 创建一个新的JavaScript文件

首先，需要创建一个新的 JavaScript 文件，例如命名为 `timeCalculation.js`。然后，将与时间计算相关的 JavaScript 代码从 HTML 文件中剪切并粘贴到这个新文件中。

**timeCalculation.js:**
```javascript
function calculateRunningTime() {
    var startDate = new Date("2018-01-01T00:00:00"); // 设置起始日期
    var now = new Date();

    // 计算时间差
    var delta = now - startDate;

    // 计算年月日时分秒
    var years = Math.floor(delta / (1000 * 60 * 60 * 24 * 365));
    delta -= years * 1000 * 60 * 60 * 24 * 365;
    var months = Math.floor(delta / (1000 * 60 * 60 * 24 * 30));
    delta -= months * 1000 * 60 * 60 * 24 * 30;
    var days = Math.floor(delta / (1000 * 60 * 60 * 24));
    delta -= days * 1000 * 60 * 60 * 24;
    var hours = Math.floor(delta / (1000 * 60 * 60));
    delta -= hours * 1000 * 60 * 60;
    var minutes = Math.floor(delta / (1000 * 60));
    delta -= minutes * 1000 * 60;
    var seconds = Math.floor(delta / 1000);

    // 更新 HTML
    document.getElementById("runningTime").innerHTML = "稳定运行 " + years + " 年 " + months + " 月 " + days + " 日 " + hours + " 时 " + minutes + " 分 " + seconds + " 秒";
}

// 页面加载完成时计算运行时间，并每秒更新一次
document.addEventListener('DOMContentLoaded', function () {
    calculateRunningTime();
    setInterval(calculateRunningTime, 1000); // 每秒更新一次
});
```

### 2. 在HTML文件中引用这个新的JavaScript文件

在您的HTML文件的`<head>`部分或`<body>`部分的底部，添加一个`<script>`标签来引用这个新的JavaScript文件。

**在HTML中添加:**
```html
<script src="timeCalculation.js"></script>
```

### 完整的HTML示例更新：
```html
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>
    <link rel="stylesheet" type="text/css" href="static/css/new_css.css">
    <link rel="icon" href="https://bornforthis.cn/favicon.ico">
    <title>AI悦创·编程1v1</title>
    <script src="timeCalculation.js"></script>
</head>
<body>
...
```

这样，您就成功地将时间计算功能独立到了一个单独的JavaScript文件中，并通过在HTML页面中引用它来调用这个功能。