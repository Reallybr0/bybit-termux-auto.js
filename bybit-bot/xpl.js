require('dotenv').config();
const { RestClientV5 } = require('bybit-api');

// Bybit Client ကို ချိတ်ဆက်ခြင်း
const client = new RestClientV5({
    key: process.env.BYBIT_API_KEY,
    secret: process.env.BYBIT_API_SECRET,
    testnet: false, // Real Account အတွက် false ထားပါ။ Testnet ဆိုရင် true ပြောင်းပါ
});

// Market Price (လက်ရှိပေါက်ဈေး) ကို ကြည့်ရန် Function
async function getMarketPrice(symbol) {
    try {
        const response = await client.getTickers({
            category: 'linear',
            symbol: symbol,
        });
        const price = response.result.list[0].lastPrice;
        console.log(`📊 ${symbol} လက်ရှိပေါက်ဈေး: ${price}`);
        return price;
    } catch (error) {
        console.error('Price ဆွဲရတာ အမှားအယွင်းရှိနေပါတယ်:', error);
    }
}

// Order တင်မည့် Function (Market Order ဖြင့် ဝယ်/ရောင်း ပြုလုပ်ခြင်း)
async function placeFutureOrder(symbol, side, qty) {
    try {
        console.log(`🚀 ${symbol} ကို ${side} Order တင်နေပါပြီ...`);
        
        const order = await client.submitOrder({
            category: 'linear',      // Futures (USDT Perpetual) အတွက် linear ကို သုံးရပါမယ်
            symbol: symbol,          // ဥပမာ - 'XPLUSDT'
            side: side,              // 'Buy' (Long) သို့မဟုတ် 'Sell' (Short)
            orderType: 'Market',     // ချက်ချင်းအလုပ်ဖြစ်စေရန် Market Order သုံးထားသည်
            qty: qty.toString(),     // Order တင်မည့် ပမာဏ (String ဖြစ်ရပါမယ်)
            timeInForce: 'GTC',
        });

        console.log('✅ Order အောင်မြင်ပါသည်!', JSON.stringify(order.result, null, 2));
    } catch (error) {
        console.error('❌ Order တင်ရတာ မအောင်မြင်ပါ:', error.message);
    }
}

// ဥပမာ အနေဖြင့် Run မည့် Main Function
async function startTrading() {
    const symbol = 'XPLUSDT'; // မိမိ Trade ချင်တဲ့ Pair (ဥပမာ XPL)
    const qty = '10';        // Trade မည့် အကြွေစေ့ ပမာဏ (XPL အစွမ်းပေါ်မူတည်၍ ပြောင်းလဲရန်)

    // ၁။ ပထမဆုံး လက်ရှိဈေးကို စစ်မယ်
    await getMarketPrice(symbol);

    // ၂။ Order တင်မယ် (စမ်းသပ်ရန်အတွက်သာ - တကယ်ဝယ်မှာဆိုရင် အောက်က Line ကို Uncomment လုပ်ပါ)
    // await placeFutureOrder(symbol, 'Buy', qty); // Long ပိုဆွဲချင်ရင် 'Buy'၊ Short ဆော့ချင်ရင် 'Sell'
}

startTrading();

