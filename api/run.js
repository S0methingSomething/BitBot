import { runFullBotProcess } from '../run-bot.js';

export default async function handler(request, response) {
  try {
    console.log(`[${new Date().toISOString()}] Vercel cron job triggered. Starting bot logic...`);
    const result = await runFullBotProcess();
    console.log(`[${new Date().toISOString()}] Bot logic finished.`);
    response.status(200).json({ status: 'OK', message: result });
  } catch (error) {
    console.error(`[${new Date().toISOString()}] An error occurred during bot execution:`, error.message);
    response.status(500).json({ status: 'Error', message: error.message });
  }
}
