require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Configuration
const token = process.env.TELEGRAM_BOT_TOKEN;
const khipuApiKey = process.env.KHIPU_API_KEY;
const khipuApiUrl = 'https://payment-api.khipu.com/v3/payments';
// Use ngrok or your public URL here. 
// For local testing, you must update this every time you restart ngrok.
const webhookUrl = process.env.WEBHOOK_URL || 'https://YOUR_NGROK_URL.ngrok-free.app/api/khipu/webhook';

if (!token) {
    console.error('TELEGRAM_BOT_TOKEN is missing in .env');
    process.exit(1);
}
if (!khipuApiKey) {
    console.error('KHIPU_API_KEY is missing in .env');
    process.exit(1);
}

// Initialize Telegram Bot
const bot = new TelegramBot(token, { polling: true });

// In-memory store for payment_id -> chat_id mapping
// In production, use a database (Redis, Postgres, etc.)
const paymentChats = new Map();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Telegram Bot Logic
bot.onText(/quiero pagar (\d+)/i, async (msg, match) => {
    const chatId = msg.chat.id;
    const amount = parseInt(match[1]);

    if (isNaN(amount) || amount <= 0) {
        bot.sendMessage(chatId, 'Por favor ingresa un monto válido.');
        return;
    }

    bot.sendMessage(chatId, `Generando link de pago por $${amount}...`);

    try {
        const transactionId = uuidv4();
        const paymentData = {
            subject: `Pago Telegram ${transactionId.substring(0, 8)}`,
            amount: amount,
            currency: 'CLP',
            transaction_id: transactionId,
            // body: 'Pago generado desde Telegram Bot', // Optional
            notifyUrl: webhookUrl,
            returnUrl: 'https://khipu.com/return', // Placeholder
            cancelUrl: 'https://khipu.com/cancel', // Placeholder
        };

        const response = await axios.post(khipuApiUrl, paymentData, {
            headers: {
                'x-api-key': khipuApiKey,
                'Content-Type': 'application/json'
            }
        });

        const { payment_id, payment_url } = response.data;

        if (payment_url) {
            // Store mapping
            paymentChats.set(payment_id, chatId);
            console.log(`Mapped payment ${payment_id} to chat ${chatId}`);

            bot.sendMessage(chatId, `Aquí está tu link de pago:\n${payment_url}`);
        } else {
            bot.sendMessage(chatId, 'Error al obtener el link de pago.');
        }

    } catch (error) {
        console.error('Error creating payment:', error.response ? error.response.data : error.message);
        bot.sendMessage(chatId, 'Hubo un error al generar el pago. Revisa los logs del servidor.');
    }
});

// Webhook Endpoint
app.post('/api/khipu/webhook', (req, res) => {
    console.log('--- Notificación de Khipu Recibida ---');
    const notificationData = req.body;

    if (!notificationData || !notificationData.payment_id) {
        console.log('Invalid notification body');
        return res.status(400).send('Bad Request');
    }

    const paymentId = notificationData.payment_id;
    const amount = notificationData.amount;
    const payerName = notificationData.payer_name;

    console.log('Notification Data:', JSON.stringify(notificationData, null, 2));

    // Check if we have a chat to notify
    if (paymentChats.has(paymentId)) {
        const chatId = paymentChats.get(paymentId);

        // If Khipu sends a notification, the payment was successful
        const message = `✅ ¡Pago recibido con éxito!\n\n` +
            `💰 Monto: $${amount} CLP\n` +
            `👤 Pagador: ${payerName}\n` +
            `🔑 ID: ${paymentId}`;

        bot.sendMessage(chatId, message);

        // Optional: Remove from map after confirming
        paymentChats.delete(paymentId);
        console.log(`Payment ${paymentId} confirmed and removed from map`);
    } else {
        console.log(`No chat found for payment ${paymentId}`);
    }

    res.status(200).send('OK');
});

app.listen(PORT, () => {
    console.log(`Servidor de Webhook escuchando en http://localhost:${PORT}`);
    console.log(`Bot de Telegram iniciado.`);
});
