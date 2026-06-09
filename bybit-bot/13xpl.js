require('dotenv').config();
const { RestClientV5 } = require('bybit-api');

const client = new RestClientV5({
    key: process.env.BYBIT_API_KEY,
    secret: process.env.BYBIT_API_SECRET,
    testnet: false, // Real Account အတွက် false ထားပါ
});

const SYMBOL = 'XPLUSDT'; 
const LEVERAGE = 74;      // 74x Leverage
const QTY = '50';         // Trade မည့် Coin ပမာဏ

// ၁။ Leverage သတ်မှတ်ခြင်း Function
async function setLeverage() {
    try {
        await client.setLeverage({
            category: 'linear',
            symbol: SYMBOL,
            buyLeverage: LEVERAGE.toString(),
            sellLeverage: LEVERAGE.toString(),
        });
        console.log(`🎯 Leverage ကို ${LEVERAGE}x သို့ ချိန်ညှိပြီးပါပြီ။`);
    } catch (error) {
        if (!error.message.includes('leverage not modified')) {
            console.error('❌ Leverage ပြောင်းလဲခြင်း မအောင်မြင်ပါ:', error.message);
        }
    }
}

// ၂။ Market Order ဖြင့် Position ဖွင့်ခြင်း (Buy/Long သို့မဟုတ် Sell/Short)
async function openPosition(side) {
    try {
        await setLeverage();
        console.log(`🚀 ${SYMBOL} ကို ${side} Order (Market) တင်နေပါပြီ...`);
        
        const order = await client.submitOrder({
            category: 'linear',
            symbol: SYMBOL,
            side: side,              // 'Buy' သို့မဟုတ် 'Sell'
            orderType: 'Market',
            qty: QTY,
            timeInForce: 'GTC',
        });

        console.log('✅ Position ကို အောင်မြင်စွာ ဖွင့်လှစ်ပြီးပါပြီ!');
        
        // Position ပွင့်သွားပြီဆိုတာနဲ့ အမြတ်/အရှုံးကို စောင့်ကြည့်မည့် Function ကို လှမ်းခေါ်မည်
        trackPnLAndAutoClose();
    } catch (error) {
        console.error('❌ Position ဖွင့်ရတာ မအောင်မြင်ပါ:', error.message);
    }
}

// ၃။ ဖွင့်ထားသော Position ကို ချက်ချင်း ပိတ်သိမ်းခြင်း (Market Close)
async function closePosition() {
    try {
        console.log(`⚠️ ${SYMBOL} Position ကို ဈေးကွက်ပေါက်ဈေးဖြင့် ပိတ်သိမ်းနေပါပြီ...`);
        
        // လက်ရှိဖွင့်ထားတဲ့ Position အခြေအနေကို စစ်ဆေးခြင်း
        const positionInfo = await client.getPositionInfo({
            category: 'linear',
            symbol: SYMBOL,
        });

        const size = parseFloat(positionInfo.result.list[0].size);
        const side = positionInfo.result.list[0].side; // 'Buy' သို့မဟုတ် 'Sell'

        if (size === 0) {
            console.log('ℹ️ လက်ရှိ ပိတ်စရာ Position မရှိပါ။');
            return;
        }

        // ရှိနေတဲ့ Position Side ရဲ့ ဆန့်ကျင်ဘက် Side ဖြင့် ပြန်ရောင်းချပြီး Position ပိတ်ခြင်း
        const closeSide = side === 'Buy' ? 'Sell' : 'Buy';

        const order = await client.submitOrder({
            category: 'linear',
            symbol: SYMBOL,
            side: closeSide,
            orderType: 'Market',
            qty: size.toString(), // ဖွင့်ထားသမျှ Size အားလုံးကို အကုန်ပိတ်မည်
            timeInForce: 'GTC',
        });

        console.log('✅ Position ကို အောင်မြင်စွာ ပိတ်သိမ်းပြီးပါပြီ!');
        process.exit(0); // Program ကို ရပ်တန့်လိုက်မည်
    } catch (error) {
        console.error('❌ Position ပိတ်သိမ်းခြင်း မအောင်မြင်ပါ:', error.message);
    }
}

// ၄။ အမြတ်/အရှုံး (PnL) ကို စောင့်ကြည့်ပြီး သတ်မှတ်ချက်ပြည့်ပါက အလိုအလျောက် ပိတ်မည့် Function
function trackPnLAndAutoClose() {
    const targetProfitROI = 20; // ဥပမာ - ၂၀% မြတ်ရင် အလိုအလျောက် ပိတ်ခိုင်းမည် (+20%)
    const maxLossROI = -15;     // ဥပမာ - ၁၅% ရှုံးရင် Stop Loss အနေဖြင့် ပိတ်ခိုင်းမည် (-15%)

    console.log('\n--- 📈 Real-time PnL စောင့်ကြည့်ခြင်း စတင်ပါပြီ ---');
    
    // ၁ စက္ကန့်လျှင် တစ်ကြိမ် PnL စစ်ဆေးမည်
    const intervalId = setInterval(async () => {
        try {
            const positionInfo = await client.getPositionInfo({
                category: 'linear',
                symbol: SYMBOL,
            });

            const pos = positionInfo.result.list[0];
            const size = parseFloat(pos.size);
            const unrealisedPnL = parseFloat(pos.unrealisedPnL); // မြတ်/ရှုံး ပမာဏ (USDT)
            const entryPrice = parseFloat(pos.entryPrice);
            const markPrice = parseFloat(pos.markPrice);

            // ဖွင့်ထားတဲ့ Position မရှိတော့ရင် စောင့်ကြည့်တာကို ရပ်မယ်
            if (size === 0) {
                console.log('ℹ️ ဖွင့်ထားသော Position မရှိတော့ပါ။ Tracking ကို ရပ်ဆိုင်းလိုက်ပါပြီ။');
                clearInterval(intervalId);
                return;
            }

            // Margin နှင့် ROI (Return on Investment %) ကို တွက်ချက်ခြင်း
            const positionMargin = (size * entryPrice) / LEVERAGE;
            const roi = (unrealisedPnL / positionMargin) * 100;

            // Terminal မှာ ပြသခြင်း
            console.clear(); // Screen ကို အမြဲရှင်းပြီး အသစ်ပဲပြပေးရန်
            console.log(`======== [ ${SYMBOL} POSITION MONITOR ] ========`);
            console.log(`Side: ${pos.side} | Size: ${size} | Entry: ${entryPrice} | Current: ${markPrice}`);
            console.log(`------------------------------------------------`);
            
            if (unrealisedPnL >= 0) {
                console.log(`🟢 Status: 🟢 မြတ်နေပါသည်!`);
            } else {
                console.log(`🔴 Status: 🔴 ရှုံးနေပါသည်!`);
            }
            
            console.log(`Profit/Loss: ${unrealisedPnL.toFixed(4)} USDT`);
            console.log(`ROI: ${roi.toFixed(2)} %`);
            console.log(`================================================`);
            console.log(`[Ctrl + C] နှိပ်ပြီး ဘော့တ်ကို အချိန်မရွေး ပိတ်နိုင်သည်။`);

            // Target ရောက်ရင် Auto ပိတ်ပေးမည့် အပိုင်း
            if (roi >= targetProfitROI) {
                console.log(`\n🎉 Target Profit (${targetProfitROI}%) ရောက်ရှိသွားသဖြင့် အလိုအလျောက် ပိတ်နေပါပြီ...`);
                clearInterval(intervalId);
                await closePosition();
            } else if (roi <= maxLossROI) {
                console.log(`\n📉 Stop Loss (${maxLossROI}%) ရောက်ရှိသွားသဖြင့် အလိုအလျောက် ပိတ်နေပါပြီ...`);
                clearInterval(intervalId);
                await closePosition();
            }

        } catch (error) {
            console.error('PnL စစ်ဆေးရတာ အမှားအယွင်းရှိပါသည်:', error.message);
        }
    }, 1000); // 1000ms = 1 Second
}

// === ၅။ ဘော့တ်ကို စတင်အသုံးပြုမည့် ပင်မနေရာ ===
async function main() {

