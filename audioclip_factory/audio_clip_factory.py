from moviepy import AudioFileClip
from moviepy import CompositeAudioClip
from moviepy import afx
from typing import Dict, Any, List, Union

class AudioClipFactory:
    """
    Factory class for creating and processing audio clips.
    """
    
    @staticmethod
    def create_audio_clip(audio_asset: Dict[str, Any]) -> AudioFileClip:
        """
        Creates an audio clip from the given asset dictionary.
        :param audio_asset: Dictionary containing audio asset parameters.
        :return: Processed AudioFileClip.
        """
        try:
            clip = AudioFileClip(audio_asset['parameters']['url'])
            return AudioClipFactory.apply_audio_effects(clip, audio_asset.get('actions', []))
        except Exception as e:
            print(f"Error loading audio file {audio_asset['parameters']['url']}: {str(e)}")
            return None
    
    @staticmethod
    def apply_audio_effects(clip: AudioFileClip, actions: List[Dict[str, Any]]) -> AudioFileClip:
        """
        Applies a series of transformations to the given audio clip based on the provided actions.
        :param clip: The audio clip to process.
        :param actions: List of actions to apply.
        :return: Processed audio clip.
        """
        for action in actions:
            if action['type'] == 'normalize_music':
                clip = clip.with_effects([afx.AudioNormalize()])
            elif action['type'] == 'loop_background_music':
                target_duration = action['param']
                start = clip.duration * 0.15
                clip = clip.subclipped(start)
                clip = clip.with_effects([afx.AudioLoop(duration=target_duration)])
            elif action['type'] == 'volume_percentage':
                clip = clip.with_effects([afx.MultiplyVolume(action['param'])])
        return clip
    
    @staticmethod
    def merge_audio_clips(audio_clips: List[AudioFileClip]) -> Union[CompositeAudioClip, None]:
        """
        Merges multiple audio clips into a single composite audio clip.
        :param audio_clips: List of AudioFileClip objects.
        :return: CompositeAudioClip if clips exist, else None.
        """
        if not audio_clips:
            return None
        return CompositeAudioClip(audio_clips)
    
    @staticmethod
    def save_audio_clip(audio_clip: AudioFileClip, output_file: str, logger=None) -> None:
        """
        Saves the audio clip to the specified output file.
        :param audio_clip: The processed audio clip.
        :param output_file: Output file path.
        :param logger: Optional logging callback.
        """
        audio_clip.fps = 44100
        if logger:
            audio_clip.write_audiofile(output_file, logger=logger)
        else:
            audio_clip.write_audiofile(output_file)
