require('dotenv').config(); // စာလုံးအသေး 'require' သို့ ပြင်ဆင်ပြီး
const { RestClientV5 } = require('bybit-api');

const client = new RestClientV5({
    key: process.env.BYBIT_API_KEY,
    secret: process.env.BYBIT_API_SECRET,
    testnet: false, 
});

const SYMBOL = 'XPLUSDT'; 
const LEVERAGE = 15;      
const QTY = '10';         

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

// ၂။ Market Order ဖြင့် Position ဖွင့်ခြင်း
async function openPosition(side) {
    try {
        await setLeverage();
        console.log(`🚀 ${SYMBOL} ကို ${side} Order (Market) တင်နေပါပြီ...`);
        
        const order = await client.submitOrder({
            category: 'linear',
            symbol: SYMBOL,
            side: side,              
            orderType: 'Market',
            qty: QTY,
            timeInForce: 'GTC',
        });

        console.log('✅ Position ကို အောင်မြင်စွာ ဖွင့်လှစ်ပြီးပါပြီ!');
        
        // စောင့်ကြည့်မည့် Function ကို ၁ စက္ကန့်ဆိုင်းပြီးမှ ခေါ်ပါမည် (API Data Update ဖြစ်ချိန်စောင့်ရန်)
        setTimeout(() => {
            trackPnLAndAutoClose();
        }, 1000);
        
    } catch (error) {
        console.error('❌ Position ဖွင့်ရတာ မအောင်မြင်ပါ:', error.message);
    }
}

// ၃။ ဖွင့်ထားသော Position ကို ချက်ချင်း ပိတ်သိမ်းခြင်း
async function closePosition() {
    try {
        console.log(`⚠️ ${SYMBOL} Position ကို ဈေးကွက်ပေါက်ဈေးဖြင့် ပိတ်သိမ်းနေပါပြီ...`);
        
        const positionInfo = await client.getPositionInfo({
            category: 'linear',
            symbol: SYMBOL,
        });

        if (!positionInfo.result.list || positionInfo.result.list.length === 0) {
            console.log('ℹ️ လက်ရှိ ပိတ်စရာ Position မရှိပါ။');
            return;
        }

        const pos = positionInfo.result.list[0];
        const size = parseFloat(pos.size);
        const side = pos.side; 

        if (size === 0 || !side) {
            console.log('ℹ️ လက်ရှိ ပိတ်စရာ Position မရှိပါ။');
            return;
        }

        const closeSide = side === 'Buy' ? 'Sell' : 'Buy';

        await client.submitOrder({
            category: 'linear',
            symbol: SYMBOL,
            side: closeSide,
            orderType: 'Market',
            qty: size.toString(), 
            timeInForce: 'GTC',
        });

        console.log('✅ Position ကို အောင်မြင်စွာ ပိတ်သိမ်းပြီးပါပြီ!');
        process.exit(0); 
    } catch (error) {
        console.error('❌ Position ปိတ်သိမ်းခြင်း မအောင်မြင်ပါ:', error.message);
    }
}

// ၄။ အမြတ်/အရှုံး (PnL) ကို စောင့်ကြည့်ပြီး သတ်မှတ်ချက်ပြည့်ပါက အလိုအလျောက် ပိတ်မည့် Function
function trackPnLAndAutoClose() {
    const targetProfitROI = 20; 
    const maxLossROI = -15;     

    console.log('\n--- 📈 Real-time PnL စောင့်ကြည့်ခြင်း စတင်ပါပြီ ---');
    
    const intervalId = setInterval(async () => {
        try {
            const positionInfo = await client.getPositionInfo({
                category: 'linear',
                symbol: SYMBOL,
            });

            if (!positionInfo.result.list || positionInfo.result.list.length === 0) {
                console.log('ℹ️ Position ရှာမတွေ့ပါ။ Tracking ကို ရပ်ဆိုင်းလိုက်ပါပြီ။');
                clearInterval(intervalId);
                return;
            }

            const pos = positionInfo.result.list[0];
            const size = parseFloat(pos.size);
            const unrealisedPnL = parseFloat(pos.unrealisedPnL || 0); 
            const entryPrice = parseFloat(pos.entryPrice || 0);
            const markPrice = parseFloat(pos.markPrice || 0);

            // Size 0 ဖြစ်သွားရင် Position မရှိတော့လို့ ရပ်မယ်
            if (size === 0) {
                console.log('ℹ️ ဖွင့်ထားသော Position မရှိတော့ပါ။ Tracking ကို ရပ်ဆိုင်းလိုက်ပါပြီ။');
                clearInterval(intervalId);
                return;
            }

            // Margin နှင့် ROI တွက်ချက်ခြင်း
            const positionMargin = (size * entryPrice) / LEVERAGE;
            const roi = positionMargin > 0 ? (unrealisedPnL / positionMargin) * 100 : 0;

            console.clear(); 
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

            // Auto Close Logic
            if (roi >= targetProfitROI) {
                console.log(`\n🎉 Target Profit (${targetProfitROI}%) ရောက်သဖြင့် ပိတ်နေပါပြီ...`);
                clearInterval(intervalId);
                await closePosition();
            } else if (roi <= maxLossROI) {
                console.log(`\n📉 Stop Loss (${maxLossROI}%) ရောက်သဖြင့် ပိတ်နေပါပြီ...`);
                clearInterval(intervalId);
                await closePosition();
            }

        } catch (error) {
            console.error('PnL စစ်ဆေးရတာ အမှားအယွင်းရှိပါသည်:', error.message);
        }
    }, 1000); 
}

// === ၅။ ဘော့တ်ကို စတင်အသုံးပြုမည့် ပင်မနေရာ (Syntax Error ပြင်ဆင်ပြီး) ===
async function main() {
    // ဖွင့်ချင်တဲ့ Position အမျိုးအစားကို ရွေးချယ်ပါ (Buy = Long / Sell = Short)
    await openPosition('Buy'); 
    
    // အရေးပေါ် ချက်ချင်းပိတ်ချင်ရင် အပေါ်က openPosition ကို comment ပိတ်ပြီး အောက်ကကောင်ကို ဖွင့်သုံးပါ
    // await closePosition();
}

main(); // Function ကို လှမ်းခေါ်ရန် ထည့်သွင်းထားသည်

