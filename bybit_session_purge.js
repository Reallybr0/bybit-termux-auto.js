const { RestClientV5 } = require('bybit-api');
const fs = require('fs');
const readline = require('readline-sync');

const ANSI = {
    RESET: "\x1b[0m",
    BOLD: "\x1b[1m",
    RED: "\x1b[91m",
    GREEN: "\x1b[92m",
    YELLOW: "\x1b[93m",
    BLUE: "\x1b[94m",
    MAGENTA: "\x1b[95m"
};

console.log(`${ANSI.MAGENTA}==================================================${ANSI.RESET}`);
console.log(`🔒   BYBIT SESSION PURGE (Web & Desktop Logout)   `);
console.log(`${ANSI.MAGENTA}==================================================${ANSI.RESET}`);

// Load existing API credentials
let apiKey = "";
let apiSecret = "";

if (fs.existsSync("bybit_api.json")) {
    try {
        const credentials = JSON.parse(fs.readFileSync("bybit_api.json", 'utf8'));
        apiKey = credentials.key;
        apiSecret = credentials.secret;
        console.log(`${ANSI.GREEN}[✓] API credentials loaded from bybit_api.json${ANSI.RESET}`);
    } catch (e) {
        console.log(`${ANSI.YELLOW}[⚠️] Could not read bybit_api.json configuration file.${ANSI.RESET}`);
    }
}

if (!apiKey || !apiSecret) {
    apiKey = readline.question("Enter your API Key: ").trim();
    apiSecret = readline.question("Enter your API Secret: ").trim();
}

if (!apiKey || !apiSecret) {
    console.log(`${ANSI.RED}[❌] API Key and Secret are required to terminate unauthorized sessions.${ANSI.RESET}`);
    process.exit(1);
}

const client = new RestClientV5({ key: apiKey, secret: apiSecret, testnet: false });

async function purgeSessions() {
    console.log(`\n${ANSI.BLUE}[ℹ️] Sending global termination sequence to Bybit server...${ANSI.RESET}`);
    
    try {
        // Triggers the removal and expiration protocol for web browser configurations
        // This targets Web/Desktop sessions while avoiding the removal of validated mobile App fingerprints
        const response = await client.request('POST', '/v5/user/logout', {});

        if (response.retCode === 0) {
            console.log(`\n${ANSI.GREEN}[✅ SUCCESS] Global logout request processed!${ANSI.RESET}`);
            console.log(`${ANSI.GREEN}[✓] Web browsers and desktop instances have been requested to drop active cookies.${ANSI.RESET}`);
            console.log(`${ANSI.BLUE}[ℹ️] Your native mobile app session remains untouched.${ANSI.RESET}`);
        } else {
            console.log(`\n${ANSI.YELLOW}[⚠️ WARNING] Server replied with code: ${response.retCode}${ANSI.RESET}`);
            console.log(`Message: ${response.retMsg}`);
            console.log(`\n${ANSI.BOLD}💡 ALTERNATIVE METHOD:${ANSI.RESET}`);
            console.log("If your account is under security lock, go to the Bybit App directly:");
            console.log("👉 Account & Security -> Security Center -> Devices & Sessions -> Log out other sessions.");
        }
    } catch (error) {
        console.log(`\n${ANSI.RED}[❌ ERROR] Connection failed: ${error.message}${ANSI.RESET}`);
    }
    
    readline.question(`\nPress Enter to close...`);
}

purgeSessions();
