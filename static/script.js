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

        suggestions.slice(0, 20).forEach(suggestion => {
            let li = document.createElement("li");
            li.textContent = suggestion.name;
            li.style.cursor = "pointer";

            // وقتی کلیک شد، به صفحه محصول برو
            li.addEventListener("click", () => {
                window.open(`product.?product_id=${suggestion.product_real_id}&store_name=${encodeURIComponent(suggestion.store)}`, "_blank");
            });

            suggestionsContainer.appendChild(li);
        });
    }

    function showPopupError(message) {
        let popup = document.createElement("div");
        popup.className = "error-popup";
        popup.textContent = message;
        document.body.appendChild(popup);

        // بعد از ۳ ثانیه پاپ‌آپ حذف شود
        setTimeout(() => {
            popup.remove();
        }, 3000);
    }
});
// داده‌های نمونه به جای فراخوانی وب سرویس
const sampleData = {
    "دیجی‌کالا": [1283496, 6156289],
    "دیجی‌استایل": [3000, 800],
    "خانومی": [2000, 600]
};

// تابع برای بارگذاری داده‌ها
function loadData() {
    const container = document.getElementById('resource-container');
    container.innerHTML = ''; // پاک کردن محتوای قبلی

    // اضافه کردن منابع به صفحه
    for (const brand in sampleData) {
        const [productCount, commentCount] = sampleData[brand];
        const resourceDiv = document.createElement('div');
        resourceDiv.className = 'resource';
        resourceDiv.innerHTML = `
            <img src="../static/${brand}.png" alt="${brand}">
            <h3>${brand}</h3>
            <div class="stats">تعداد محصولات: ${productCount}</div>
            <div class="stats">تعداد کامنت‌ها: ${commentCount}</div>
        `;
        container.appendChild(resourceDiv);
    }
}

