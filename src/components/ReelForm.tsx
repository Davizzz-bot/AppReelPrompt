import React, { useState } from 'react';

interface ReelFormProps {
  onSubmit: (prompt: string) => void;
}

const ReelForm: React.FC<ReelFormProps> = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState<string>('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(prompt);
    setPrompt('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt here"
        className="border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
      <button
        type="submit"
        className="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600"
      >
        Generate Reel
      </button>
    </form>
  );
};

export default ReelForm;