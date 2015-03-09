
import click
from dem import dem as demlib


@click.command('dem')
@click.argument('srcpath', type=click.Path(exists=True))
@click.argument('dstpath', type=click.Path(exists=False))
def dem(srcpath, dstpath):
    demlib.toDigitalElevationModel(srcpath, dstpath)


if __name__ == '__main__':
    dem()