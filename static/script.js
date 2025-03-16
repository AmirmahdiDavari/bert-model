
document.addEventListener("DOMContentLoaded", function () {
    const searchBox = document.querySelector(".search-box");
    const suggestionsContainer = document.querySelector(".suggestions");

    searchBox.addEventListener("keyup", function () {
        let query = searchBox.value.trim();

        // فقط وقتی که تعداد کاراکترهای ورودی بیش از ۲ باشد جستجو انجام شود
        if (query.length > 2) {
            fetchSuggestions(query);
        } else {
            suggestionsContainer.innerHTML = "";
        }
    });

        function fetchSuggestions(query) {
            fetch(`http://localhost:8000/search/?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("خطا در دریافت اطلاعات از سرور!");
                    }
                    console.error(response)
                    return response.json();
                })
                .then(data => {
                    displaySuggestions(data);
                })
                .catch(error => {
                    showPopupError(error.message);
                    console.error("خطا در دریافت داده‌ها:", error);
                });
        }

        function displaySuggestions(suggestions) {
            suggestionsContainer.innerHTML = ""; // پاک کردن پیشنهادات قبلی

            if (suggestions.length === 0) {
                suggestionsContainer.innerHTML = "<li>هیچ پیشنهادی یافت نشد</li>";
                return;
            }
            console.log(suggestions.slice(0, 5))
            suggestions.slice(0, 5).forEach(suggestion => {
                let li = document.createElement("li");
                li.textContent = suggestion.name;
                li.onclick = () => alert(`مورد انتخابی: ${suggestion.name}`);
                suggestionsContainer.appendChild(li);
            });
        }

        function showPopupError(message) {
            let popup = document.createElement("div");
            popup.className = "error-popup";
            popup.textContent = message;
            document.body.appendChild(popup);

            // بعد از ۵ ثانیه پاپ‌آپ حذف شود
            setTimeout(() => {
                popup.remove();
            }, 3000);
        }
        });