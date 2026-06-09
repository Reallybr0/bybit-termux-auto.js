const ccxt = require('ccxt');

const exchange = new ccxt.bybit({
    'apiKey': 'MPPuDtw9KyhK444kjA',
    'secret': 'Gjd40IENlCNX3e2zuxCnO7YFVcvhyuZWHxw2',
    'options': { 'defaultType': 'future' } // Future Trading အတွက်
});

async function fetchStatus() {
    try {
        console.log("--- Bybit Trading Status ---");
        
        // ၁။ Balance စစ်ဆေးခြင်း
        const balance = await exchange.fetchBalance();
        console.log(`လက်ကျန်ငွေ (Balance): ${balance.total.USDT} USDT`);

        // ၂။ အဖွင့်အနေအထား (Positions) နှင့် အမြတ်/ရှုံး စစ်ဆေးခြင်း
        const positions = await exchange.fetchPositions();
        positions.forEach(pos => {
            if (parseFloat(pos.contracts) > 0) {
                console.log(`\nCurrency: ${pos.symbol}`);
                console.log(`အမြတ်/ရှုံး (Unrealized PnL): ${pos.unrealizedPnl} USDT`);
                console.log(`လက်ရှိအရေအတွက် (Qty): ${pos.contracts}`);
            }
        });
        
    } catch (e) {
        console.log("Error ဖြစ်သည် - API Key သို့မဟုတ် Permission စစ်ဆေးပါ:", e.message);
    }
}

// ၅ စက္ကန့်တိုင်း အလိုအလျောက် ပြသပေးမည်
setInterval(fetchStatus, 5000);

