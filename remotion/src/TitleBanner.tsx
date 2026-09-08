import React from 'react';
import { interpolate, spring, useCurrentFrame } from 'remotion';

interface TitleBannerProps {
  title: string;
  fps: number;
}

export const TitleBanner: React.FC<TitleBannerProps> = ({ title, fps }) => {
  const frame = useCurrentFrame();

  // Show during first 3.5 seconds
  const endFrame = Math.round(3.5 * fps);
  if (frame > endFrame) return null;

  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 120 },
  });

  const opacity = interpolate(
    frame,
    [endFrame - 15, endFrame],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        position: 'absolute',
        top: 140,
        left: 0,
        width: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 50,
        opacity,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          backgroundColor: 'rgba(255, 230, 0, 0.95)',
          padding: '12px 28px',
          borderRadius: 8,
          border: '4px solid #000',
          boxShadow: '6px 6px 0px #000',
          maxWidth: '85%',
          textAlign: 'center',
        }}
      >
        <span
          style={{
            fontFamily: "'Impact', 'Arial Black', sans-serif",
            fontSize: 34,
            textTransform: 'uppercase',
            letterSpacing: 1.5,
            color: '#000',
            lineHeight: 1.2,
          }}
        >
          {title}
        </span>
      </div>
    </div>
  );
};
