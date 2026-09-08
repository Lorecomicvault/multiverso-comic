import React from 'react';
import { Audio, useCurrentFrame, useVideoConfig, staticFile, Video } from 'remotion';
import { WordSubtitle } from './WordSubtitle';
import { TitleBanner } from './TitleBanner';
import type { VideoCompositionProps, WordTiming } from './types';

const CHUNK_SIZE = 3; // 2-3 words per phrase for ultra-punchy TikTok/Reels reading

export const VideoComposition: React.FC<VideoCompositionProps> = ({
  subtitleData,
  title,
  videoSrc = 'concatenated.mp4',
  audioSrc = 'voiceover_full.mp3',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = subtitleData?.words || [];

  // Group words into short 2-3 word chunks
  const chunks: WordTiming[][] = [];
  let currentChunk: WordTiming[] = [];
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    if (currentChunk.length === 0) {
      currentChunk.push(w);
    } else {
      const prev = currentChunk[currentChunk.length - 1];
      const gap = w.start - prev.end;
      if (currentChunk.length >= CHUNK_SIZE || gap > 0.4) {
        chunks.push(currentChunk);
        currentChunk = [w];
      } else {
        currentChunk.push(w);
      }
    }
  }
  if (currentChunk.length > 0) chunks.push(currentChunk);

  // Find active chunk for current frame
  const currentTime = frame / fps;
  const activeChunk = chunks.find((chunk) => {
    const first = chunk[0];
    const last = chunk[chunk.length - 1];
    return currentTime >= first.start - 0.05 && currentTime <= last.end + 0.25;
  });

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        backgroundColor: '#0a0a0f',
        overflow: 'hidden',
      }}
    >
      {/* Background Video (Composed scene with blurred backdrop + full panel) */}
      <Video
        src={staticFile(videoSrc)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
        muted
      />

      {/* Synchronized Narration Audio */}
      <Audio src={staticFile(audioSrc)} />

      {/* Comic Story Title Banner (first 3.5s) */}
      {title && <TitleBanner title={title} fps={fps} />}

      {/* Subtitles Overlay: Positioned safely at bottom: 440px (above UI icons) */}
      {activeChunk && (
        <div
          style={{
            position: 'absolute',
            bottom: 440,
            left: 0,
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            flexWrap: 'wrap',
            padding: '0 24px',
            boxSizing: 'border-box',
            zIndex: 40,
          }}
        >
          <div
            style={{
              display: 'inline-flex',
              justifyContent: 'center',
              alignItems: 'center',
              flexWrap: 'wrap',
              backgroundColor: 'rgba(0, 0, 0, 0.45)',
              padding: '8px 20px',
              borderRadius: 14,
              border: '2px solid rgba(255, 230, 0, 0.4)',
              backdropFilter: 'blur(4px)',
            }}
          >
            {activeChunk.map((word, idx) => (
              <WordSubtitle
                key={`${word.text}_${idx}_${word.start}`}
                word={word}
                fps={fps}
                frame={frame}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
