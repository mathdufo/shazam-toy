# shazam-toy

shazam-toy is a toy-implementation of the [shazam audio identification algorithm](https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf). It's heavily inspired by [dejavu](https://github.com/worldveil/dejavu) and [abracadabra](https://github.com/notexactlyawe/abracadabra). 

## Usage
### Register
You first need to create a database and fill it with a directory containing your audio samples in .wav format.

``` bash
shazam-toy register -wav_directory path_to_wav_directory
```
You can also include info (eg. lyrics, album, date, etc) for each sample by making a directory filled with .txt file matching your .wav files (abc.wav and abc.txt).

``` bash
shazam-toy register -wav_directory path_to_wav_directory -txt_directory path_to_txt_directory
```
### Identification
You can identify an audio sample

``` bash
shazam-toy identify -f path_to_sample
```

Or identify a sample from your microphone

``` bash
shazam-toy identify -m -d duration
```

The output has the following format
```
Name: Name of the audio sample
Confidence: How likely the result is to be right 
Time: The time at which the audio sample started. Could be an array if the audio repeats.
Info: The optional information from the .txt file
```

## Example
This is an example using the album Yeezus by Kanye West. We fill the database with 2 directory: yeezus/yeezus_wav/ and yeezus/yeezus_txt/. The former contains the songs in .wav and the latter contains 
the lyrics in .txt.

``` bash
shazam-toy register -wav_directory yeezus/yeezus_wav/ -txt_directory yeezus/yeezus_txt/
```

You can  identify the file yeezus/noisy 5 second Bound 2.wav
``` bash
shazam-toy identify -f yeezus/noisy 5 second Bound 2.wav
```

You can also use your microphone and identify any song on the album
``` bash
shazam-toy identify -m -d 10
```


## Performance
The performance are about what you would expect from a toy-implementation.
(performance.png)