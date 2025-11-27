document.addEventListener('DOMContentLoaded', () => {
    const showFormBtn = document.getElementById('show-form-btn');
    const formContainer = document.getElementById('order-form-container');
    const categorySelect = document.getElementById('category-select');
    const productSelect = document.getElementById('product-select');
    const priceInput = document.getElementById('price');
    const amountInput = document.getElementById('amount');
    const totalInput = document.getElementById('total');
    const orderForm = document.getElementById('order-form');

    // 顯示表單
    showFormBtn.addEventListener('click', () => {
        formContainer.style.display = 'block';
    });

    // 選擇分類後更新商品名稱
    categorySelect.addEventListener('change', async () => {
        const category = categorySelect.value;
        if (!category) return;
        const res = await fetch(`/product?category=${encodeURIComponent(category)}`);
        const data = await res.json();
        productSelect.innerHTML = '<option value="">--請選擇商品--</option>';
        data.product.forEach(p => {
            const option = document.createElement('option');
            option.value = p;
            option.textContent = p;
            productSelect.appendChild(option);
        });
        priceInput.value = '';
        totalInput.value = '';
    });

    // 選擇商品後自動取得單價
    productSelect.addEventListener('change', async () => {
        const product = productSelect.value;
        if (!product) return;
        const res = await fetch(`/product?product=${encodeURIComponent(product)}`);
        const data = await res.json();
        priceInput.value = data.price;
        countTotal();
    });

    // 數量變動自動計算小計
    amountInput.addEventListener('input', countTotal);

    function countTotal() {
        const price = parseFloat(priceInput.value) || 0;
        const amount = parseInt(amountInput.value) || 1;
        totalInput.value = price * amount;
    }

    // 表單送出
    orderForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(orderForm);
        const res = await fetch('/product', {
            method: 'POST',
            body: formData
        });
        if (res.redirected) {
            window.location.href = res.url;
        }
    });

    // 刪除訂單
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const orderId = btn.dataset.id;
            if (!confirm('確定刪除嗎?')) return;
            const res = await fetch(`/product?order_id=${orderId}`, { method: 'DELETE' });
            if (res.ok) window.location.reload();
        });
    });
});
