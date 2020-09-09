# video-timer
This is a simple openCV code that puts a timer in a video

## Usage

Input file must be a `.mp4` 60fps file.

```{shell}
python video-timer.py --position "tr" --src_file "./test.mp4" --init_time "9.8" --end_time "31" 
```

Possible arguments:

* `--position`: top-right ("tr"), top-left ("tl"), bottom-right ("br"), bottom-left ("bl").
* `--src_file`: relative path to the video file.
* `--init_time`: Time in which the timer starts in the video, expresed in seconds with decimals. 
* `--end_time`: Time in which the timer stops in the video, expresed in seconds with decimals. 
* `--show_minutes` (optional): Whether the timer should show minutes or not, False by default.
