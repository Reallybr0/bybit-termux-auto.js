const { RestClientV5 } = require('bybit-api');
const fs = require('fs');
const readline = require('readline-sync');

// ANSI Color Codes
const ANSI = {
    RESET: "\x1b[0m",
    BOLD: "\x1b[1m",
    RED: "\x1b[91m",
    GREEN: "\x1b[92m",
    YELLOW: "\x1b[93m",
    BLUE: "\x1b[94m",
    MAGENTA: "\x1b[95m"
};

const SPOT_SYMBOL = "OPGUSDT";
const SPOT_COIN = "OPG";
const TRADE_AMOUNT_USDT = 5; // တစ်ခါဝယ်ရင် 5 USDT ဖိုး
const VOLUME_TARGET = 1000;  // ပစ်မှတ် Volume $1000

console.log(`${ANSI.MAGENTA}==================================================${ANSI.RESET}`);
console.log(`🚀      BYBIT OPG SPOT VOLUME BOT ($1000 TARGET)  `);
console.log(`${ANSI.MAGENTA}==================================================${ANSI.RESET}`);

// API Credentials ယူခြင်း
let apiKey = "";
let apiSecret = "";

if (fs.existsSync("bybit_api.json")) {
    try {
        const credentials = JSON.parse(fs.readFileSync("bybit_api.json", 'utf8'));
        apiKey = credentials.key;
        apiSecret = credentials.secret;
        console.log(`${ANSI.GREEN}[✓] API Key & Secret Loaded successfully.${ANSI.RESET}`);
    } catch (e) {
        console.log(`${ANSI.RED}[❌] API Configuration Error.${ANSI.RESET}`);
    }
}

if (!apiKey || !apiSecret) {
    apiKey = readline.question("Enter your API Key: ").trim();
    apiSecret = readline.question("Enter your API Secret: ").trim();
}

const client = new RestClientV5({ key: apiKey, secret: apiSecret, testnet: false });

// ဖုန်းထဲက OPG လက်ကျန် ဘယ်လောက်ရှိလဲ စစ်သည့် Function
async function getOpgBalance() {
    try {
        const res = await client.getWalletBalance({ accountType: 'UNIFIED', coin: SPOT_COIN });
        if (res.retCode === 0 && res.result.list[0].coin[0]) {
            return parseFloat(res.result.list[0].coin[0].walletBalance) || 0.0;
        }
    } catch (e) {
        return 0.0;
    }
    return 0.0;
}

async function startVolumeBot() {
    let currentVolume = 0.0;
    console.log(`\n${ANSI.BLUE}[ℹ️] Target Volume: $${VOLUME_TARGET}${ANSI.RESET}`);
    console.log(`${ANSI.BLUE}[ℹ️] Running OPG/USDT pairs on Bybit Spot...${ANSI.RESET}\n`);

    while (currentVolume < VOLUME_TARGET) {
        try {
            console.log(`${ANSI.BOLD}--------------------------------------------------${ANSI.RESET}`);
            // ၁။ အဝယ် (Buy Orders) $5 ဖိုး လှမ်းဝယ်ခြင်း
            console.log(`${ANSI.BLUE}[🛒] Buying $${TRADE_AMOUNT_USDT} worth of OPG...${ANSI.RESET}`);
            const buyRes = await client.submitOrder({
                category: 'spot',
                symbol: SPOT_SYMBOL,
                side: 'Buy',
                orderType: 'Market',
                qty: TRADE_AMOUNT_USDT.toString()
            });

            if (buyRes.retCode === 0) {
                currentVolume += TRADE_AMOUNT_USDT;
                console.log(`${ANSI.GREEN}[✅ BUY SUCCESS] Volume တက်လာပြီ: $${currentVolume.toFixed(2)}${ANSI.RESET}`);
            } else {
                console.log(`${ANSI.RED}[⚠️ BUY FAILED] ${buyRes.retMsg}${ANSI.RESET}`);
            }

            // စက္ကန့်ပိုင်း ခြားပေးခြင်း (Bybit Server က Rate Limit မမိအောင်)
            await new Promise(resolve => setTimeout(resolve, 3000));

            // ၂။ အရောင်း (Sell Orders) လက်ရှိရှိတဲ့ OPG အကုန် ပြန်ရောင်းခြင်း
            const opgBal = await getOpgBalance();
            if (opgBal > 0.1) { // OPG အရေအတွက် ရှိမှ ရောင်းမည်
                console.log(`${ANSI.YELLOW}[⚖️] Selling ${opgBal} OPG back to USDT...${ANSI.RESET}`);
                const sellRes = await client.submitOrder({
                    category: 'spot',
                    symbol: SPOT_SYMBOL,
                    side: 'Sell',
                    orderType: 'Market',
                    qty: opgBal.toString()
                });

                if (sellRes.retCode === 0) {
                    currentVolume += TRADE_AMOUNT_USDT;
                    console.log(`${ANSI.GREEN}[✅ SELL SUCCESS] Volume တက်လာပြီ: $${currentVolume.toFixed(2)}${ANSI.RESET}`);
                } else {
                    console.log(`${ANSI.RED}[⚠️ SELL FAILED] ${sellRes.retMsg}${ANSI.RESET}`);
                }
            }

            // နောက်တစ်ကျော့ မသွားခင် ၄ စက္ကန့် စောင့်ခြင်း
            await new Promise(resolve => setTimeout(resolve, 4000));

        } catch (error) {
            console.log(`${ANSI.RED}[❌ ERROR] Network Exception: ${error.message}${ANSI.RESET}`);
            await new Promise(resolve => setTimeout(resolve, 5000)); // Error တက်ရင် ၅ စက္ကန့် နားမည်
        }
    }

    console.log(`\n${ANSI.MAGENTA}==================================================${ANSI.RESET}`);
    console.log(`${ANSI.GREEN}[🎉 TARGET ACHIEVED] OPG Spot Volume $${currentVolume.toFixed(2)} ပြည့်သွားပြီဖြစ်၍ Bot ကို ရပ်ဆိုင်းလိုက်ပါပြီ။${ANSI.RESET}`);
    console.log(`${ANSI.MAGENTA}==================================================${ANSI.RESET}`);
}

startVolumeBot();

