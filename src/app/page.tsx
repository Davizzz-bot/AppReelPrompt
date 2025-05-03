import React from 'react';
import PromptInput from '../components/PromptInput';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold text-center mb-10">
        Reel Generator
      </h1>
      <PromptInput />
    </main>
  );
}