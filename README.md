<div align="center">
<h1>comic-tools</h1>

A buncha tools for properly naming comic and manga images in archives.
</div>

## Intro

A lot of manga archives are named in a way that makes it difficult do automated tasks with.  
Many other archives are formatted nicely, and these tools are meant to help you get your archives to that point.  

### What is a "nice" format?

The "nice" format is as follows:  
`SERIES - cXXX (vYY) - pZZZ.jpg`  
So, for example, a chapter of Cool Story have its images named:  
`Cool Story - c001 (v01) - p001.jpg`  
`Cool Story - c001 (v01) - p002.jpg`  
`...`

Additional "nice" things to add would be tags like `[Cover]`, `[Padding]`, `[ToC]`, etc. at the end of the filename.  
Because these can be done manually and aren't utterly necessary, I haven't taken the time to automate them.

## Requirements

- Python 3+

## Usage

Run `main.py` and follow the prompts.

## The Tools

1. [Rename Volume Files](#rename-volume-files)
2. [Convert Folder to CBZ](#convert-folder-to-cbz)
3. [Split Volume into Chapters](#split-volume-into-chapters)
4. [Convert Volumes to CBV](#convert-volumes-to-cbv)

### Rename Volume Files

This option will run perform three actions in order to rename the images in a volume to the "nice" format.
In this process, we'll be using volume 1 of a manga called "Cool Story" as an example.

1. Reset  
"Reset" the image filenames to a sequential order  
`cool_story_001.jpg` will become `00001.jpg`
2. Pages  
Set the filenames to the `SERIES - cXXX (vYY) - pZZZ` format  
`00001.jpg` will become `Cool Story - cXXX (v01) - p001.jpg`
3. Chapters  
Use `chapters.csv` (see [below](#chapterscsv)) to set the chapter numbers of the images
`Cool Story - cXXX (v01) - p001.jpg` will become `Cool Story - c001 (v01) - p001.jpg`

#### chapters.csv

This file is used to set the chapter numbers of the images by counting the pages as they're read and checking when the chapter changes.  
The format is as follows:

```csv
001,000
002,017
003,035
004,053
```

\**note: the first chapter should almost always start at 000*

### Convert Folder to CBZ

This process will take a directory of images and convert them to a CBZ file.
A folder that looks like

```plaintext
Cool Story v01
├── Cool Story - c001 (v01) - p001.jpg
├── Cool Story - c001 (v01) - p002.jpg
├── Cool Story - c001 (v01) - p003.jpg
¦
└── Cool Story - cXXX (v01) - pZZZ.jpg
```

and make it into a zip file called  
`Cool Story v01.cbz`

### Split Volume into Chapters

This process will take a volume .CBZ file (or directory of CBZ files) and them into chapters.  
`Cool Story v01.cbz`  
will become  
`Cool Story - c001 (v01).cbz`  
`Cool Story - c002 (v01).cbz`  
`...`

### Convert Volumes to CBV

Based on [a format proposal of sorts that I made](https://github.com/Jordy3D/CBViewer), this process will take a directory of chapters and convert them to CBV files.
A folder that looks like

```plaintext
Cool Story
├── Cool Story - Chapter 001 (v01).cbz
├── Cool Story - Chapter 002 (v01).cbz
├── Cool Story - Chapter 003 (v01).cbz
¦
└── Cool Story - Chapter XXX (vYY).cbz
```

and make it into a zip file called  
`Cool Story v01.cbv`  
which internally looks like

```plaintext
Cool Story v01.cbv
├── Cool Story - Chapter 001 (v01).cbz
├── Cool Story - Chapter 002 (v01).cbz
├── Cool Story - Chapter 003 (v01).cbz
¦
└── Cool Story - Chapter XXX (v01).cbz
```

## Notes

- Spreads are not automatically detected if they're not already joined. If you process a volume that has unmarked spreads, it *may* mess up the page count, causing the chapter numbers to be off.
- Some chapters or volumes may need an additional empty page before various points in the chapter (primarily the table of contents), otherwise the page count may be off.  
  - Before doing any processing related to chapters, make sure that the page numbers you provide are accurate to the files you're processing.
