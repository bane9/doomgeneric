# ======= RISCVBox benchmark program

This program is designed to benchmark RISCVBox, Spike, and QEMU for my master's thesis. Instead of rendering DOOM to a framebuffer, the program outputs to the console whenever a frame is rendered, with frame delays removed. This adjustment was necessary because Spike and QEMU lack accurate time reporting, leading to incorrect results in benchmarks like CoreMark. Therefore, all benchmarking had to be performed on the host side.

To build this project, first install the RISC-V GNU toolchain. Then, navigate to the doomgeneric folder and run the following commands:
```bash
make iwad
make # For baremetal
make linux # For Linux build
```

This repo provides a script that runs a command as a subprocess, filters its output for a specified word, and logs the timestamps (in nanoseconds, relative to the first occurrence) to `output.csv`. The script can be found in `doomgeneric/timestamp_csv.py`

**Usage:** 
```bash
python3 capture_output.py "./start-qemu-bare.sh" "doom_draw"
```

**Note:**
This repository also includes the demo version of doom 1, located in doomgeneric/doom1.iwad

# ======= Original README below
# doomgeneric
The purpose of doomgeneric is to make porting Doom easier.
Of course Doom is already portable but with doomgeneric it is possible with just a few functions.

To try it you will need a WAD file (game data). If you don't own the game, shareware version is freely available (doom1.wad).

# porting
Create a file named doomgeneric_yourplatform.c and just implement these functions to suit your platform.
* DG_Init
* DG_DrawFrame
* DG_SleepMs
* DG_GetTicksMs
* DG_GetKey

|Functions            |Description|
|---------------------|-----------|
|DG_Init              |Initialize your platfrom (create window, framebuffer, etc...).
|DG_DrawFrame         |Frame is ready in DG_ScreenBuffer. Copy it to your platform's screen.
|DG_SleepMs           |Sleep in milliseconds.
|DG_GetTicksMs        |The ticks passed since launch in milliseconds.
|DG_GetKey            |Provide keyboard events.
|DG_SetWindowTitle    |Not required. This is for setting the window title as Doom sets this from WAD file.

### main loop
At start, call doomgeneric_Create().

In a loop, call doomgeneric_Tick().

In simplest form:
```
int main(int argc, char **argv)
{
    doomgeneric_Create(argc, argv);

    while (1)
    {
        doomgeneric_Tick();
    }
    
    return 0;
}
```

# sound
Sound is much harder to implement! If you need sound, take a look at SDL port. It fully supports sound and music! Where to start? Define FEATURE_SOUND, assign DG_sound_module and DG_music_module.

# platforms
Ported platforms include Windows, X11, SDL, emscripten. Just look at (doomgeneric_win.c, doomgeneric_xlib.c, doomgeneric_sdl.c).
Makefiles provided for each platform.

## emscripten
You can try it directly here:
https://ozkl.github.io/doomgeneric/

emscripten port is based on SDL port, so it supports sound and music! For music, timidity backend is used.

## Windows
![Windows](screenshots/windows.png)

## X11 - Ubuntu
![Ubuntu](screenshots/ubuntu.png)

## X11 - FreeBSD
![FreeBSD](screenshots/freebsd.png)

## SDL
![SDL](screenshots/sdl.png)
