import React, { useRef, useState } from 'react';

interface ReelPreviewProps {
  videoUrl: string;
}

const ReelPreview: React.FC<ReelPreviewProps> = ({ videoUrl }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="reel-preview-container">
      <video
        ref={videoRef}
        src={videoUrl}
        className="reel-video"
        onClick={handlePlayPause}
        controls
      />
    </div>
  );
};

export default ReelPreview;