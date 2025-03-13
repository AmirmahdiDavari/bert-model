function checkWords() {
    let input = document.querySelector(".search-box").value;
    let words = input.trim().split(/\s+/);
    if (words.length >= 2) {
        alert("مقدار وارد شده: " + input);
    }
}
