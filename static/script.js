
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
            console.log(suggestions.slice(0, 20))
            suggestions.slice(0, 20).forEach(suggestion => {
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

// // تابع برای بارگذاری داده‌ها از وب سرویس
// async function loadData() {
//     try {
//         const response = await fetch('get_mraket_analisist');
//         const data = await response.json();
//
//         const container = document.getElementById('resource-container');
//         container.innerHTML = ''; // پاک کردن محتوای قبلی
//         const  data={
//             "دیجی‌کالا": [5000, 1200],
//             "دیجی‌استایل": [3000, 800],
//             "خانومی": [2000, 600]} ;
//
//         // اضافه کردن منابع به صفحه
//         for (const brand in data) {
//             const [productCount, commentCount] = data[brand];
//             const resourceDiv = document.createElement('div');
//             resourceDiv.className = 'resource';
//             resourceDiv.innerHTML = `
//                 <img src="../static/${brand}.png" alt="${brand}">
//                 <h3>${brand}</h3>
//                 <div class="stats">تعداد محصولات: ${productCount}</div>
//                 <div class="stats">تعداد کامنت‌ها: ${commentCount}</div>
//             `;
//             container.appendChild(resourceDiv);
//         }
//     } catch (error) {
//         console.error('Error fetching data:', error);
//     }
// }
//
// // بارگذاری داده‌ها هنگام بارگذاری صفحه
// window.onload = loadData;

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

// بارگذاری داده‌ها هنگام بارگذاری صفحه
window.onload = loadData;
document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:8000/market_report/")
        .then(response => {
            if (!response.ok) {
                throw new Error("مشکلی در دریافت داده‌ها رخ داده است");
            }
            return response.json();
        })
        .then(data => {
            const container = document.getElementById("resource-container");
            container.innerHTML = ""; // پاک کردن محتوای قبلی

            data.forEach(item => {
                const resourceDiv = document.createElement("div");
                resourceDiv.classList.add("resource");

                resourceDiv.innerHTML = `
                    <h3>${item.market_name}</h3>
                    <p>${item.total_products}</p>
                    <p>${item.total_reviews}</p>
                `;
                container.appendChild(resourceDiv);
            });
        })
        .catch(error => {
            console.error("خطا در دریافت اطلاعات: ", error);
        });
});