const clickBtn = document.getElementById("clickBtn");
const message = document.getElementById("message");

let count = 0;

clickBtn.addEventListener("click", function () {
    count++;
    message.textContent = "你已经点击了 " + count + " 次按钮！";
});