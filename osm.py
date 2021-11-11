#!/usr/bin/python
from sys import argv
import os
import math
import requests
import os.path


class OSMTileDownloader():
    # Tile servers (check arguments x y z and modify downloadTile() for the tile server below)
    # http://tile.openstreetmap.org/{z}/{x}/{y}.png
    tileServerOSM = 'http://a.tile.openstreetmap.org'
    # http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png
    tileServerWorld = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile'
    # Type = 'osm' or 'world'
    defaultType = 'osm'
    # Path to save tiles folder
    localPath = 'tiles-library'

    def __init__(self, argv):
        print('OSM Downloader started')
        try:
            # Retrive arguments
            _, lat0, lng0, lat1, lng1, minZoom, maxZoom, type = argv
            self.defaultType = type
        except:
            print('Invalid arguments. Check example below:')
            print(
                '**********************************************************************************')
            print(
                'python osm.py <start lat> <start lng> <finish lat> <finish lng> <min zoom> <max zoom> <type>')
            print('python osm.py 34.979067 23.350545 35.485885 26.310979 0 6 osm')
            print('python osm.py 34.979067 23.350545 35.485885 26.310979 7 10 world')
            print(
                '**********************************************************************************')
            exit(2)

        if int(minZoom) < int(maxZoom):
            if int(minZoom) <= 6:
                # Check upper boundary
                m1Zoom = maxZoom
                if int(m1Zoom) > 6:
                    m1Zoom = 6
                # From 0 to 6 download all tiles
                for zoom in range(int(minZoom), int(m1Zoom) + 1, 1):
                    # Start downloading
                    print('T1 - Zoom: %d, All Tiles' % zoom)
                    for x in range(0, 2**zoom, 1):
                        for y in range(0, 2**zoom, 1):
                            self.downloadTile(zoom, x, y)
            if int(maxZoom) >= 7:
                # Check lower boundary
                m2Zoom = minZoom
                if int(m2Zoom) < 7:
                    m2Zoom = 7
                # From 7 to max zoom
                for zoom in range(int(m2Zoom), int(maxZoom) + 1, 1):
                    # Convert degress to number
                    xtile, ytile = self.deg2num(float(lat0), float(lng0), zoom)
                    final_xtile, final_ytile = self.deg2num(
                        float(lat1), float(lng1), zoom)
                    # Start downloading
                    print('T2 - Zoom: %d, Tiles X: %d to %d to Y %d to %d' %
                          (zoom, xtile, final_xtile, ytile, final_ytile))
                    for x in range(xtile, final_xtile + 1, 1):
                        for y in range(ytile, final_ytile - 1, -1):
                            self.downloadTile(zoom, x, y)
        else:
            print('Invalid zoom levels')
            exit(2)

    # Convert degress to number of tile
    def deg2num(self, latDeg, lngDeg, zoom):
        latRad = math.radians(latDeg)
        n = 2.0 ** zoom
        xTile = int((lngDeg + 180.0) / 360.0 * n)
        yTile = int((1.0 - math.log(math.tan(latRad) +
                                    (1 / math.cos(latRad))) / math.pi) / 2.0 * n)
        return (xTile, yTile)

    # Download tile in .png format from
    def downloadTile(self, zoom, xtile, ytile):
        if(self.defaultType == 'osm'):
            # OSM Tiles
            # Use non-secure connection
            url = '%s/%d/%d/%d.png' % (self.tileServerOSM, zoom, xtile, ytile)
            directoryPath = '%s/tiles/%d/%d/' % (self.localPath, zoom, xtile)
            downloadPath = '%s/tiles/%d/%d/%d.png' % (
                self.localPath, zoom, xtile, ytile)
        elif(self.defaultType == 'world'):
            # World Imagery Tiles
            # Use non-secure connection
            url = '%s/%d/%d/%d.png' % (self.tileServerWorld,
                                       zoom, ytile, xtile)
            directoryPath = '%s/tiles/%d/%d/' % (self.localPath, zoom, ytile)
            downloadPath = '%s/tiles/%d/%d/%d.png' % (
                self.localPath, zoom, ytile, xtile)
        else:
            exit(2)

        # Make directory if not exists
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)

        if(not os.path.isfile(downloadPath)):
            print('Downloading tile: %r' % url)
            data = requests.get(url).content
            # Save data to local storage
            with open(downloadPath, 'wb') as handler:
                handler.write(data)
                handler.close()
        else:
            print('Skipped tile: %r' % url)


def main(argv):
    try:
        OSMTileDownloader(argv)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(argv)
