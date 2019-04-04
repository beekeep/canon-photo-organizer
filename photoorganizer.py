import os
import shutil
import argparse
import glob
import exifread
import timeit

__author__ = 'mnessen'


def main(**kwargs):
    for key, value in kwargs.iteritems():
        print key, value
    photoDir = kwargs['inDir']
    outputDir = kwargs['outDir']
    photos = []
    for (dirpath, dirnames, filenames) in os.walk(photoDir):
        for file in glob.fnmatch.filter(filenames, '*.[jJ][pP][gG]'):
            photos.append(os.path.join(dirpath, file))
        for file in glob.fnmatch.filter(filenames, '*.[cC][rR]2'):
            photos.append(os.path.join(dirpath, file))
        # break
    starttime = timeit.default_timer()
    processphotos(photos, outputDir)
    runtime = timeit.default_timer() - starttime
    print('Copied %s photos in %s' % (len(photos), runtime))


def processphotos(files, outDir):
    for photo in files:
        f = open(photo, 'rb')
        try:
            tags = exifread.process_file(f)
            if tags:
                photoDateTime = str(tags['EXIF DateTimeOriginal'])
                photoDate = photoDateTime.split(' ')[0].split(":")
                f.close()
                # print photoDate
                destPath = ensurePathExists(photoDate[0], photoDate[1], photoDate[2], outDir)
                try:
                    shutil.copyfile(photo, os.path.join(destPath, os.path.basename(photo)))
                except OSError:
                    raise
        finally:
            f.close()

def ensurePathExists(year, month, day, outDir):
    yearPath = os.path.join(outDir, year)
    monthPath = os.path.join(yearPath, month)
    dayPath = os.path.join(monthPath, day)
    # make sure year dir exists
    try:
        os.makedirs(yearPath)
    except OSError:
        if not os.path.isdir(yearPath):
            raise
    # make sure month path exists
    try:
        os.makedirs(monthPath)
    except OSError:
        if not os.path.isdir(monthPath):
            raise
    # make sure day path exists
    try:
        os.makedirs(dayPath)
    except OSError:
        if not os.path.isdir(dayPath):
            raise
    return dayPath


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something', version='%(prog)s 1.0')
    parser.add_argument('inDir', type=str, help='Input directory')
    parser.add_argument('outDir', type=str, help='Output directory')
    args = parser.parse_args()
    main(**vars(args))
