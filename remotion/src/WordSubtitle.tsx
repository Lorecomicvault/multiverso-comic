import React from 'react';
import { interpolate, spring } from 'remotion';
import type { WordTiming } from './types';

interface WordSubtitleProps {
  word: WordTiming;
  fps: number;
  frame: number;
}

export const WordSubtitle: React.FC<WordSubtitleProps> = ({ word, fps, frame }) => {
  const wordStartFrame = Math.round(word.start * fps);
  const wordEndFrame = Math.round(word.end * fps);

  const isActive = frame >= wordStartFrame && frame < wordEndFrame;
  const isPast = frame >= wordEndFrame;

  // Kinetic pop animation when active
  const popSpring = spring({
    frame: Math.max(0, frame - wordStartFrame),
    fps,
    config: { damping: 10, stiffness: 180 },
  });

  const scale = isActive ? interpolate(popSpring, [0, 1], [0.95, 1.18]) : 1.0;
  const color = isActive ? '#FFE600' : '#FFFFFF';

  return (
    <span
      style={{
        display: 'inline-block',
        transform: `scale(${scale})`,
        transformOrigin: 'center bottom',
        fontSize: 52,
        fontWeight: 900,
        fontFamily: "'Impact', 'Arial Black', sans-serif",
        fontStyle: 'italic',
        letterSpacing: '1.5px',
        color,
        textTransform: 'uppercase',
        WebkitTextStroke: '3.5px #000',
        textShadow: `
          0px 0px 12px rgba(0,0,0,0.95),
          4px 4px 0px #000,
          -4px -4px 0px #000,
          4px -4px 0px #000,
          -4px 4px 0px #000
        `,
        margin: '0 6px',
        transition: 'transform 0.05s ease-out',
      }}
    >
      {word.text}
    </span>
  );
};
