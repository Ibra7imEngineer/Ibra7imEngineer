const menuData = [
    { id: 1, name: "تشيز برجر لارج", price: 95, img: "https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 2, name: "بيتزا ايطاليانو", price: 130, img: "https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 3, name: "باستا وايت صوص", price: 90, img: "https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 4, name: "وجبة دجاج كريسبي", price: 160, img: "https://images.pexels.com/photos/2232433/pexels-photo-2232433.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 5, name: "كريب زنجر حار", price: 85, img: "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 6, name: "بيتزا بيبروني", price: 140, img: "https://images.pexels.com/photos/4109111/pexels-photo-4109111.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 7, name: "ساندوتش كفتة مشوية", price: 75, img: "https://images.pexels.com/photos/5950444/pexels-photo-5950444.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 8, name: "حواوشي اسكندراني", price: 65, img: "https://images.pexels.com/photos/2097090/pexels-photo-2097090.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 9, name: "موهيتو ليمون نعناع", price: 50, img: "https://images.pexels.com/photos/338713/pexels-photo-338713.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 10, name: "آيس كوفي فانيليا", price: 65, img: "https://images.pexels.com/photos/2615323/pexels-photo-2615323.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 11, name: "عصير برتقال فريش", price: 40, img: "https://images.pexels.com/photos/2109099/pexels-photo-2109099.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 12, name: "ميلك شيك شوكولاتة", price: 75, img: "https://images.pexels.com/photos/103566/pexels-photo-103566.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 13, name: "فراولة باللبن", price: 55, img: "https://images.pexels.com/photos/808941/pexels-photo-808941.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 14, name: "كابتشينو ساخن", price: 45, img: "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 15, name: "تشيز كيك توت", price: 70, img: "https://images.pexels.com/photos/1126359/pexels-photo-1126359.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 16, name: "مولتن كيك دافئ", price: 80, img: "https://images.pexels.com/photos/45202/brownie-dessert-cake-sweet-45202.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 17, name: "كريب نوتيلا موز", price: 85, img: "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 18, name: "دوناتس مشكل", price: 50, img: "https://images.pexels.com/photos/1191639/pexels-photo-1191639.jpeg?auto=compress&cs=tinysrgb&w=500" },
    { id: 19, name: "آيس كريم فواكه", price: 45, img: "https://images.pexels.com/photos/1362534/pexels-photo-1362534.jpeg?auto=compress&cs=tinysrgb&w=500" },
   
];

let cart = [];
const deliveryFee = 20;

function renderMenu(items) {
    const grid = document.getElementById('menuGrid');
    if (!grid) return;
    grid.innerHTML = items.map(p => `
        <div class="card">
            <div class="img-box"><img src="${p.img}"></div>
            <h3>${p.name}</h3>
            <p class="price-text">${p.price} ج.م</p>
            <button class="add-btn" onclick="addToCart(${p.id})">إضافة للطلب</button>
        </div>
    `).join('');
}

function addToCart(id) {
    const product = menuData.find(p => p.id === id);
    const item = cart.find(i => i.id === id);
    item ? item.qty++ : cart.push({ ...product, qty: 1 });
    updateUI();
    toggleCart(true); 
}

function updateQuantity(id, change) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += change;
        if (item.qty <= 0) cart = cart.filter(i => i.id !== id);
        updateUI();
    }
}

function updateUI() {
    const list = document.getElementById('cartItemsList');
    const totalDisplay = document.getElementById('totalDisplay');
    const cartCount = document.getElementById('cartCount');

    cartCount.innerText = cart.reduce((sum, item) => sum + item.qty, 0);
    let subtotal = 0;
    list.innerHTML = cart.map(item => {
        subtotal += item.price * item.qty;
        return `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:10px; border-bottom:1px solid #eee;">
                <div><b>${item.name}</b><br><small>${item.price} ج.م</small></div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <button onclick="updateQuantity(${item.id}, -1)">-</button>
                    <span>${item.qty}</span>
                    <button onclick="updateQuantity(${item.id}, 1)">+</button>
                </div>
            </div>`;
    }).join('');

    const finalTotal = cart.length > 0 ? subtotal + deliveryFee : 0;
    totalDisplay.innerHTML = `
        <div style="font-size:14px;">الطلبات: ${subtotal} ج.م</div>
        <div style="font-size:14px;">التوصيل: ${cart.length > 0 ? deliveryFee : 0} ج.م</div>
        <div style="font-size:18px; font-weight:bold; margin-top:5px;">الإجمالي: ${finalTotal} ج.م</div>
    `;
    totalDisplay.dataset.val = finalTotal;
}

function toggleCart(show) {
    document.getElementById('cartSidebar').classList.toggle('active', show);
    document.getElementById('overlay').style.display = show ? 'block' : 'none';
}

function sendOrderWhatsApp() {
    const name = document.getElementById('custName').value.trim();
    const phone = document.getElementById('custPhone').value.trim(); 
    const addr = document.getElementById('custAddress').value.trim();

    if (!name || !phone || !addr) {
        alert("يا فندم، يرجى إكمال بياناتك (الاسم، الموبايل، العنوان)");
        return;
    }
    if (cart.length === 0) { alert("يا فندم، السلة فارغة!"); return; }

    let message = `*طلب جديد للمدير (New Order)* 🔔\n\n`;
    message += `👤 *العميل:* ${name}\n📱 *موبايل:* ${phone}\n📍 *العنوان:* ${addr}\n`;
    message += `--------------------------\n*الأصناف:*\n`;
    cart.forEach(item => { message += `• ${item.name} (x${item.qty}) = ${item.price * item.qty} ج.م\n`; });
    message += `--------------------------\n🚚 *التوصيل:* ${deliveryFee} ج.م\n💰 *الإجمالي:* ${document.getElementById('totalDisplay').dataset.val} ج.م`;

    const adminNumber = "201229965943"; // رقمك يا فندم
    window.location.href = `https://api.whatsapp.com/send?phone=${adminNumber}&text=${encodeURIComponent(message)}`;
}

window.onload = () => {
    renderMenu(menuData);
    document.getElementById('searchInput').addEventListener('input', (e) => {
        renderMenu(menuData.filter(p => p.name.includes(e.target.value)));
    });
};