## Description
AudioDeviceCmdlets is a suite of PowerShell Cmdlets to control audio devices on Windows


## Features
Get list of all audio devices  
Get default audio device (playback/recording)  
Get default communication audio device (playback/recording)  
Get volume and mute state of default audio device (playback/recording)  
Get volume and mute state of default communication audio device (playback/recording)  
Set default audio device (playback/recording)  
Set default communication audio device (playback/recording)  
Set volume and mute state of default audio device (playback/recording)  
Set volume and mute state of default communication audio device (playback/recording)



## Usage
```PowerShell
Get-AudioDevice -ID <string>			# Get the device with the ID corresponding to the given <string>
Get-AudioDevice -Index <int>			# Get the device with the Index corresponding to the given <int>
Get-AudioDevice -List				# Get a list of all enabled devices as <AudioDevice>
Get-AudioDevice -PlaybackCommunication		# Get the default communication playback device as <AudioDevice>
Get-AudioDevice -PlaybackCommunicationMute	# Get the default communication playback device's mute state as <bool>
Get-AudioDevice -PlaybackCommunicationVolume	# Get the default communication playback device's volume level on 100 as <float>
Get-AudioDevice	-Playback			# Get the default playback device as <AudioDevice>
Get-AudioDevice -PlaybackMute			# Get the default playback device's mute state as <bool>
Get-AudioDevice -PlaybackVolume			# Get the default playback device's volume level on 100 as <float>
Get-AudioDevice -RecordingCommunication		# Get the default communication recording device as <AudioDevice>
Get-AudioDevice -RecordingCommunicationMute	# Get the default communication recording device's mute state as <bool>
Get-AudioDevice -RecordingCommunicationVolume	# Get the default communication recording device's volume level on 100 as <float>
Get-AudioDevice -Recording			# Get the default recording device as <AudioDevice>
Get-AudioDevice -RecordingMute			# Get the default recording device's mute state as <bool>
Get-AudioDevice -RecordingVolume		# Get the default recording device's volume level on 100 as <float>
```
```PowerShell
Set-AudioDevice	<AudioDevice>				# Set the given playback/recording device as both the default device and the default communication device, for its type
Set-AudioDevice <AudioDevice> -CommunicationOnly	# Set the given playback/recording device as the default communication device and not the default device, for its type
Set-AudioDevice <AudioDevice> -DefaultOnly		# Set the given playback/recording device as the default device and not the default communication device, for its type
Set-AudioDevice -ID <string>				# Set the device with the ID corresponding to the given <string> as both the default device and the default communication device, for its type
Set-AudioDevice -ID <string> -CommunicationOnly		# Set the device with the ID corresponding to the given <string> as the default communication device and not the default device, for its type
Set-AudioDevice -ID <string> -DefaultOnly		# Set the device with the ID corresponding to the given <string> as the default device and not the default communication device, for its type
Set-AudioDevice -Index <int>				# Set the device with the Index corresponding to the given <int> as both the default device and the default communication device, for its type
Set-AudioDevice -Index <int> -CommunicationOnly		# Set the device with the Index corresponding to the given <int> as the default communication device and not the default device, for its type
Set-AudioDevice -Index <int> -DefaultOnly		# Set the device with the Index corresponding to the given <int> as the default device and not the default communication device, for its type
Set-AudioDevice -PlaybackCommunicationMuteToggle	# Set the default communication playback device's mute state to the opposite of its current mute state
Set-AudioDevice -PlaybackCommunicationMute <bool>	# Set the default communication playback device's mute state to the given <bool>
Set-AudioDevice -PlaybackCommunicationVolume <float>	# Set the default communication playback device's volume level on 100 to the given <float>
Set-AudioDevice -PlaybackMuteToggle			# Set the default playback device's mute state to the opposite of its current mute state
Set-AudioDevice -PlaybackMute <bool>			# Set the default playback device's mute state to the given <bool>
Set-AudioDevice -PlaybackVolume <float>			# Set the default playback device's volume level on 100 to the given <float>
Set-AudioDevice -RecordingCommunicationMuteToggle	# Set the default communication recording device's mute state to the opposite of its current mute state
Set-AudioDevice -RecordingCommunicationMute <bool>	# Set the default communication recording device's mute state to the given <bool>
Set-AudioDevice -RecordingCommunicationVolume <float>	# Set the default communication recording device's volume level on 100 to the given <float>
Set-AudioDevice -RecordingMuteToggle			# Set the default recording device's mute state to the opposite of its current mute state
Set-AudioDevice -RecordingMute <bool>			# Set the default recording device's mute state to the given <bool>
Set-AudioDevice -RecordingVolume <float>		# Set the default recording device's volume level on 100 to the given <float>
```
```PowerShell
Write-AudioDevice -PlaybackCommunicationMeter	# Write the default playback device's power output on 100 as a meter
Write-AudioDevice -PlaybackCommunicationStream	# Write the default playback device's power output on 100 as a stream of <int>
Write-AudioDevice -PlaybackMeter		# Write the default playback device's power output on 100 as a meter
Write-AudioDevice -PlaybackStream		# Write the default playback device's power output on 100 as a stream of <int>
Write-AudioDevice -RecordingCommunicationMeter	# Write the default recording device's power output on 100 as a meter
Write-AudioDevice -RecordingCommunicationStream	# Write the default recording device's power output on 100 as a stream of <int>
Write-AudioDevice -RecordingMeter		# Write the default recording device's power output on 100 as a meter
Write-AudioDevice -RecordingStream		# Write the default recording device's power output on 100 as a stream of <int>
```


