import React, { useState } from 'react';
import ReelForm from '../components/ReelForm';
import ReelPreview from '../components/ReelPreview';

export default function Home() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const handleVideoGenerated = (url: string) => {
    setVideoUrl(url);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold text-center mb-10">
        Reel Generator
      </h1>
      <ReelForm onVideoGenerated={handleVideoGenerated} />
      {videoUrl && <ReelPreview videoUrl={videoUrl} />}
    </main>
  );
}