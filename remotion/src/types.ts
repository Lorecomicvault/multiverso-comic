export interface WordTiming {
  text: string;
  start: number;
  end: number;
}

export interface SubtitleData {
  fps: number;
  words: WordTiming[];
}

export interface VideoCompositionProps {
  subtitleData: SubtitleData;
  title?: string;
  width?: number;
  height?: number;
  videoSrc?: string;
  audioSrc?: string;
}
