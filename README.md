# Reel Generator App

This project is a web application that allows users to create reels. The user provides a prompt to the web application, then the application uses the OpenAI and DALLE APIs to generate a script and images, after that it synthesizes a voiceover using Firebase Functions, Storage and Hosting, and finally assembles the video to show it to the user. This is the high level architecture of the app:

<CODE_BLOCK>

There is an image that should be added later.

</CODE_BLOCK> 


This project leverages the power of Next.js, Firebase, and various AI APIs to create engaging and dynamic video content.

## Functionalities

1.  **Text Input:** Users can input a text prompt or description.
2.  **Script Generation (OpenAI):** The application uses the OpenAI API (GPT-4) to generate a detailed script based on the user's input.
3.  **Image Generation (DALL·E/Stable Diffusion):** Relevant images are generated based on the script using DALL·E or Stable Diffusion APIs.
4.  **Voice-over Synthesis (ElevenLabs/Google TTS):** The script is converted into voice-over audio using ElevenLabs or Google Text-to-Speech APIs.
5.  **Video Assembly (Node.js + ffmpeg):** Images and audio are combined into a vertical video reel (9:16 aspect ratio) using a backend process with Node.js and ffmpeg.
6.  **Preview and Download:** Users can preview the generated reel and download the video.

## Code Structure

*   **`src/app`:** Next.js pages directory.
*   **`src/components`:** React components used in the UI.
*   **`src/lib`:** Reusable libraries and utilities.
*   **`src/functions`:** Firebase Functions containing the backend logic.
*   **`public`:** Static assets.
*   **`firebase.json` and `.firebaserc`:** Firebase configuration files.

## How to use

1.  Clone the repository.
2.  Set up a Firebase project and add the necessary credentials to `src/lib/firebase.ts`.
3.  Install dependencies: `npm install`.
4.  Start the Next.js development server: `npm run dev`.
5.  Access the application in your browser: `http://localhost:3000`.

## Next steps

*   Set up the OpenAI API.
*   Set up the DALLE API.
*   Set up Firebase Functions.
*   Set up Firebase Storage.
*   Set up Firebase Hosting.
*   Create the user interface to input prompts.
* Create the logic for the steps of the flow.
