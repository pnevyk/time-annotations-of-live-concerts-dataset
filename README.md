# Time Annotations of Live Concerts Dataset

This repository attempts to compile a dataset of time annotations of songs in live concerts which can be found around
the web. This information can be then used by people who want to do some music/sound information retrieval analysis. Due
to copyright rights conformity, this repository doesn't contain actual audio files, only links to these files (mostly
video-sharing sites) and corresponding annotations.

## Help Appreciated

The bigger this dataset is, the better for any analysis. However, annotating concerts requires some manual work.
Nevertheless, this work is quite simple (although boring) and no special knowledge is necessary. Therefore everyone can
help build this dataset, and I do appreciate any eventual help.

### Submitting

#### GitHub

If you have GitHub account, you can submit your annotations either via
[issues](https://github.com/pnevyk/time-annotations-of-live-concerts-dataset/issues) or by opening a
[pull request](https://github.com/pnevyk/time-annotations-of-live-concerts-dataset/pulls) where you add annotation file
and update `data/index.csv` file accordingly.

#### Google Forms

For non-GitHub users there is a simple [Google form](https://goo.gl/forms/GRxmIRuDcRC9bzFd2).

#### Guidelines

All annotations files are placed in `data/` directory. There is also `index.csv` file in `data/` directory which
contains metadata for all concerts. Times are in simple `h:mm:ss` format, each song on new line and consisting of two
these times separated by space. Metadata for each concert are:

* **Name** &ndash; User friendly name of the concert. It should be the band name and optionally the venue and the year
of recording. Example: *Red Hot Chili Peppers - Rock In Rio Lisboa 2006*.
* **File** &ndash; Same as *Name*, but in lowercase and with hyphens instead of spaces. Example:
*red-hot-chili-peppers-rock-in-rio-lisboa-2006*.
* **Link** &ndash; Link to the audio of the concert. Example: *https://www.youtube.com/watch?v=BUZmNViNgxA*.
* **Genre** &ndash; Currently, there are no restrictions, but it should be a reasonably high level label. Example:
*Funk Rock*.
* **Audio Quality** &ndash; The are no clear borders, it is an approximate label. There are three possible value:
*Good* (high quality recording), *Average* (recording using reasonable equipment or old recording), *Bad* (amateur
recording or old recording using non-professional equipment). *Concerts of all types of audio quality are desired!*

##### Boundaries

Sometimes, it is quite difficult and unclear how to determine where song actually starts or ends. Below are some vague
recommendations which may be extended in the future:

* When song is started by drummer's stick clicking, the boundary is placed on the first click
* When song ends with fade out
  * If the fade out is ended with a loud hit, the boundary is placed on this hit
  * Otherwise, the boundary is placed on the start of the fade out

## Using

There is a small Python script which handles basic data retrieving.

### Install

The script requires `ffmpeg` installed on your system.

```bash
# clone this repository, you can use name of your choice
git clone git@github.com:pnevyk/time-annotations-of-live-concerts-dataset.git talc
# go to the repo directory
cd talc
# install python package to be available in your scripts, name of the package is `talc`
pip install .
```

### Usage

```python
import talc

# get metadata
talc.get_metadata()
# => pandas dataframe representation of data/index.csv file

# get all concerts names and corresponding audio file paths
talc.get_audio_list()
# => [('AC/DC - Capital Centre 1981', '<path to repository>/.audio/acdc-capital-centre-1981.wav'), ...]
# you can alter destination directory via TALC_AUDIO_DIRECTORY environment variable
# if audio files are not present in the destination directory, they are automatically downloaded
# this process may take a while

# get audio file path to one concert
talc.get_audio_filepath('Metallica - Moscow 1991')
# => <path to repository>/.audio/metallica-moscow-1991.wav
# again, you can alter destination directory via TALC_AUDIO_DIRECTORY environment variable

# get time annotations for a concert
talc.get_time_annotations('Metallica - Moscow 1991')
# => [(0, 304), (328, 784), ...]
# by default, these times are in seconds
# if you want to get human readable times, call this function with `seconds` argument set to False
```

# License

All time annotations are released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license. By
submitting your annotation you are agreeing that it will be available under this license. Please submit only your work
or work which is publicly available on the web.
