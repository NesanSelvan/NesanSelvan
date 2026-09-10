## Nesan Selvan

Software engineer. I build **[NutriScan](https://nutriscan.app/)** end to end — the vision and language pipeline, the Python services, the Flutter app, and the infrastructure under all three.

## NutriScan

**Point a camera at a plate, get the nutrition back.** Leading full-stack development since June 2024.

[![Play Store](https://img.shields.io/badge/Google_Play-100K%2B_downloads-1a1a1a?style=flat-square&logo=googleplay&logoColor=white)](https://play.google.com/store/apps/details?id=app.nutriscan)
[![App Store](https://img.shields.io/badge/App_Store-4.4★_·_432_ratings-1a1a1a?style=flat-square&logo=appstore&logoColor=white)](https://apps.apple.com/in/app/nutriscan-calorie-diet-plan/id6479204257)
[![Site](https://img.shields.io/badge/nutriscan.app-1a1a1a?style=flat-square)](https://nutriscan.app/)

**Meal scan.** The photo goes to a vision model that pulls out every food item and its portion, then a language model turns that into full macros and micros and grades the meal A–E. It streams back over a WebSocket as it resolves, so nobody watches a spinner.

**NutriBites.** A retrieval assistant answering questions against your own history — text-to-SQL over your logged meals, vector search over a nutrition knowledge base.

**Monika.** A voice nutritionist you talk to hands-free, running natively in the app.

**28-day diet plans.** Generated per user from their BMR, TDEE and goal — two options per meal slot, plus the grocery list to shop it.

**Goal-aware tracking.** Weight loss, muscle gain, diabetes, PCOS, pregnancy and illness recovery each change what the app measures and what it tells you.

**The weekly leaderboard.** Rewritten after the first formula rewarded raw volume — 17 lunches a day beat five good meals. The score now caps spam, rewards distinct meal slots, and penalises eating past your macro targets.

**The platform underneath.** FastAPI on Cloud Run, PostgreSQL on Supabase, Firebase, Apple Health and Google Fit sync, home-screen widgets, over-the-air Flutter updates, 12 languages. 99.8% uptime.

## Also building

**[DevCLI](https://github.com/NesanSelvan/devcli)** — a local-first terminal for the Claude Code era: a real shell plus a panel holding your prompt vault, agents, skills and MCP servers. Rust, Tauri, xterm.

**[Agents Space](https://github.com/NesanSelvan/Agents-Space)** — infinite canvas workspace for AI agents. Run terminals, edit files, orchestrate coding agents side by side.

**Flutter packages on pub.dev** — [wiggle_kit](https://pub.dev/packages/wiggle_kit) · [tooltip_pro](https://pub.dev/packages/tooltip_pro) · [haptic_feedback_pro](https://pub.dev/packages/haptic_feedback_pro)

## Writing

- [Fine-tuning Qwen2.5-VL with Unsloth](https://medium.com/@nesan4selvan/fine-tuning-qwen2-5-vl-with-unsloth-a-complete-guide-to-vision-language-model-training-7d2445374cc8)
- [Personalised chatbots with LlamaIndex](https://medium.com/@nesan4selvan/personalized-chatbots-using-llamaindex-bridging-database-with-ai-08995c731c8f)
- [In-app purchases in Flutter for Android](https://medium.com/stackademic/implementing-in-app-purchases-in-flutter-for-android-a-step-by-step-guide-72f7973ef8e0)

## Tools

Python · Dart / Flutter · TypeScript · Rust · SQL · PostgreSQL · Supabase · Firebase · GCP · Docker · LlamaIndex

## Elsewhere

[Website](https://nesanselvan.netlify.app/) · [LinkedIn](https://www.linkedin.com/in/nesan-selvan-305669217/) · [Medium](https://medium.com/@nesan4selvan) · [nesanselvan004@gmail.com](mailto:nesanselvan004@gmail.com)
