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
            print("🎵 Successfully loaded audio file.")
            return AudioClipFactory.apply_audio_effects(clip, audio_asset.get('actions', []))
        except Exception as e:
            print(f"❌ Error loading audio file {audio_asset['parameters']['url']}: {str(e)}")
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
                print("🎚️ Applying normalization effect.")
                clip = AudioClipFactory.normalize_music(clip)
            elif action['type'] == 'loop_background_music':
                print("🔄 Looping background music.")
                clip = AudioClipFactory.loop_background_music(clip, action['param'])
            elif action['type'] == 'volume_percentage':
                print(f"🔊 Adjusting volume by {action['param']*100}%. ")
                clip = AudioClipFactory.adjust_volume(clip, action['param'])
        return clip
    
    @staticmethod
    def normalize_music(clip: AudioFileClip) -> AudioFileClip:
        """Applies normalization to the audio clip."""
        return clip.with_effects([afx.AudioNormalize()])
    

    @staticmethod
    def loop_background_music(clip: AudioFileClip, target_duration: float) -> AudioFileClip:
        """Loops the background music to match a target duration, adjusting volume dynamically."""
        start = clip.duration * 0.15
        clip = clip.subclipped(start, clip.duration)
        clip = clip.with_effects([afx.AudioLoop(duration=target_duration)])
        print(f"🔂 Music looped to {target_duration} seconds.")
        
        # Enhanced Dynamic Volume Adjustment using while loop
        max_volume_threshold = 0.3  # Upper threshold
        min_volume_threshold = 0.1  # Lower threshold
        smoothing_factor = 0.1  # Prevent extreme fluctuations
        
        volume_factor = 1.0
        detected_volume = clip.max_volume()
        
        while detected_volume > max_volume_threshold or detected_volume < min_volume_threshold:
            if detected_volume > max_volume_threshold:
                volume_factor *= max_volume_threshold / detected_volume * (1 - smoothing_factor)
                print(f"📉 Volume too high ({detected_volume:.2f}), reducing it smoothly.")
            elif detected_volume < min_volume_threshold:
                volume_factor *= min_volume_threshold / detected_volume * (1 + smoothing_factor)
                print(f"📈 Volume too low ({detected_volume:.2f}), increasing it smoothly.")
            
            clip = AudioClipFactory.adjust_volume(clip, volume_factor)
            detected_volume = clip.max_volume()
        
        print("✅ Volume is within the acceptable range.")
        return clip

    @staticmethod
    def adjust_volume(clip: AudioFileClip, factor: float) -> AudioFileClip:
        """Adjusts the volume of the audio clip by a given factor."""
        print(f"🔊 Adjusting volume by a factor of {factor:.2f}.")
        return clip.with_effects([afx.MultiplyVolume(factor)])
    
    @staticmethod
    def merge_audio_clips(audio_clips: List[AudioFileClip]) -> Union[CompositeAudioClip, None]:
        """
        Merges multiple audio clips into a single composite audio clip.
        :param audio_clips: List of AudioFileClip objects.
        :return: CompositeAudioClip if clips exist, else None.
        """
        if not audio_clips:
            print("⚠️ No audio clips to merge.")
            return None
        print("🎶 Merging multiple audio clips into one.")
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
        print(f"💾 Saving audio clip to {output_file}.")
        if logger:
            audio_clip.write_audiofile(output_file, logger=logger)
        else:
            audio_clip.write_audiofile(output_file)
