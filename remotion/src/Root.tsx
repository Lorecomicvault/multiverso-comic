import React from 'react';
import { registerRoot, Composition, getInputProps } from 'remotion';
import { VideoComposition } from './VideoComposition';
import type { VideoCompositionProps } from './types';

const inputProps = (getInputProps() || {}) as VideoCompositionProps & {
  width?: number;
  height?: number;
};

const Root: React.FC = () => {
  const { subtitleData, title, width = 1080, height = 1920 } = inputProps;
  const fps = subtitleData?.fps || 30;

  const lastWord = subtitleData?.words?.[subtitleData.words.length - 1];
  const lastTime = lastWord ? lastWord.end : 30;
  const durationInFrames = Math.max(90, Math.ceil(lastTime * fps) + fps);

  return (
    <Composition
      id="VideoComposition"
      component={VideoComposition}
      durationInFrames={durationInFrames}
      fps={fps}
      width={width}
      height={height}
      defaultProps={inputProps}
    />
  );
};

registerRoot(Root);
