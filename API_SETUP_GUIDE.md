# FRIDAY Ultra — API Setup Guide

## 1. Google Calendar + Gmail API (Ek hi credential sabke liye)

**Step 1**: https://console.cloud.google.com/ → Login
**Step 2**: Top par "Select a project" → "New Project" → Naam daalo "FRIDAY"
**Step 3**: Left menu → "APIs & Services" → "Library"
**Step 4**: Search karo "Google Calendar API" → Enable
**Step 5**: Search karo "Gmail API" → Enable
**Step 6**: Left menu → "Credentials" → "Create Credentials" → "OAuth client ID"
**Step 7**: "Configure Consent Screen" → "External" → App name "FRIDAY" → Apna email → Save
**Step 8**: Wapas "Credentials" → "Create Credentials" → "OAuth client ID" → "Desktop app" → "FRIDAY"
**Step 9**: "Download JSON" → Save as `google_credentials.json` in FRIDAY folder
**Step 10**: `.env` file mein daalo:
```
GOOGLE_CREDENTIALS_PATH=google_credentials.json
```

## 2. Spotify API

**Step 1**: https://developer.spotify.com/dashboard/ → Login with Spotify
**Step 2**: "Create App" → App name "FRIDAY" → Description "Voice assistant" → Create
**Step 3**: Client ID aur Client Secret dikhega → Copy karo
**Step 4**: "Edit Settings" → "Redirect URIs" → Add `http://localhost:8888/callback` → Save
**Step 5**: `.env` mein daalo:
```
SPOTIFY_CLIENT_ID=tumhara_client_id
SPOTIFY_CLIENT_SECRET=tumhara_client_secret
```

## 3. WhatsApp API (Meta Cloud API - Free)

**Step 1**: https://developers.facebook.com/ → Login
**Step 2**: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
**Step 3**: "Get Started" → "Create App" → "Business" type → App name "FRIDAY"
**Step 4**: WhatsApp → "Set Up" → "Send and Receive Messages"
**Step 5**: Apna phone number verify karo (jo WhatsApp hai)
**Step 6**: "Temporary Access Token" copy karo (24 ghante chalta hai, baad mein permanent token generate karo)
**Step 7**: Phone Number ID bhi copy karo
**Step 8**: `.env` mein:
```
WHATSAPP_TOKEN=tumhara_token
WHATSAPP_PHONE_ID=tumhara_phone_number_id
WHATSAPP_TO=tumhara_number_jisko_msg_dena
```

## 4. Weather API (WeatherAPI - Free tier 1M calls/month)

**Step 1**: https://www.weatherapi.com/signup → Signup (email + password)
**Step 2**: Login karo → Dashboard pe API key dikhega
**Step 3**: `.env` mein daalo:
```
WEATHERAPI_KEY=tumhari_api_key
```

## 5. ElevenLabs Voice Cloning (Optional - Premium Feature)

**Step 1**: https://elevenlabs.io → Signup
**Step 2**: Subscription choose karo (free tier bhi hai limited characters)
**Step 3**: Profile → "API Keys" → "Generate New Key"
**Step 4**: `.env` mein daalo:
```
ELEVENLABS_API_KEY=tumhari_api_key
```

## Final .env file structure

```
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=AIza...
GOOGLE_API_KEY=AIza...
ANTHROPIC_API_KEY=sk-ant-...
NVIDIA_API_KEY=nvapi-...
GROQ_API_KEY=gsk_...
DEEPSEEK_API_KEY=sk-...
OPENCODE_API_KEY=sk-...
GOOGLE_CREDENTIALS_PATH=google_credentials.json
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
WHATSAPP_TOKEN=...
WHATSAPP_PHONE_ID=...
WEATHERAPI_KEY=...
ELEVENLABS_API_KEY=...
```

**🔥 Best part**: Jab sab keys aa jayengi, main ek hi baar mein saare features implement kar dunga — Calendar, Email, Spotify, WhatsApp, Weather, Voice Cloning — sab ek sath. Batao pehle kaunsi keys mil gayi?
