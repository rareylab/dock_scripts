"""Grid generation for DOCK workflow"""
import argparse
import configparser
import logging
import os

from pipeline import PipelineElement


# intentionally sparse interface pylint: disable=too-few-public-methods
class Grid(PipelineElement):
    """Grid generation for DOCK workflow"""

    def __init__(self, active_site, spheres, output, config):
        """Grid generation for DOCK workflow

        :param active_site: active site mol2 file
        :param spheres: selected spheres file
        :param output: output directory to write to
        :param config: config object
        """
        self.active_site = active_site
        self.spheres = spheres
        self.output = output
        self.config = config
        self.grid = None

    def run(self):
        """Run grid generation"""
        if not os.path.exists(self.output):
            os.mkdir(self.output)

        box = self.__create_box()
        self.grid = self.__create_grid(box)

    def __create_box(self):
        box = os.path.join(self.output, 'box.pdb')
        with open('box.in.template') as box_template:
            box_in = box_template.read()
        box_in = box_in.replace('{spheres}', self.spheres)
        box_in = box_in.replace('{box}', box)
        PipelineElement._commandline(
            [self.config['Binaries']['showbox']],
            input=bytes(box_in, 'utf8')
        )
        return box

    def __create_grid(self, box):
        grid = os.path.join(self.output, 'grid')
        with open('grid.in.template') as grid_template:
            grid_in = grid_template.read()
        grid_in = grid_in.replace('{active_site}', self.active_site)
        grid_in = grid_in.replace('{box}', box)
        grid_in = grid_in.replace('{vdw}', self.config['Parameters']['vdw'])
        grid_in = grid_in.replace('{grid}', grid)
        grid_in_path = os.path.join(self.output, 'grid.in')
        with open(grid_in_path, 'w') as grid_in_file:
            grid_in_file.write(grid_in)
        args = [
            self.config['Binaries']['grid'],
            '-i', grid_in_path
        ]
        PipelineElement._commandline(args)
        return grid


def main(args):
    """Module main to demonstrate functionality"""
    logging.basicConfig(level=logging.DEBUG)
    config = configparser.ConfigParser()
    config.read(args.config)
    grid = Grid(args.active_site, args.spheres, args.output, config)
    grid.run()
    print(grid.grid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('active_site', type=str, help='path to the active site')
    parser.add_argument('spheres', type=str, help='path to the spheres')
    parser.add_argument('output', type=str, help='output directory to write spheres')
    parser.add_argument('--config', type=str, help='path to a config file', default='config.ini')
    main(parser.parse_args())