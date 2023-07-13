"""Console script for decomnano."""
import sys
import click
from .decomnano import DecomNano
from .sweep import SweepDecomNano
import toml
import numpy as np


def parse_array_in_config(config_dict):
    """Parse array in config file to numpy array."""

    if "input_config" not in config_dict:
        return config_dict

    for key, value in config_dict["input_config"].items():
        if isinstance(value, dict):
            config_dict["input_config"][key] = np.arange(
                value["start"],
                value["end"],
                value["step"],
            )

    return config_dict


def run_sweep(
    config_dict=None, output="result.csv", interval=100, kernel=None, resolution=0.1
):
    """Run SweepDecomNano with config_dict."""

    config_dict = parse_array_in_config(config_dict)
    
    if config_dict["fix_bulk_fraction"]:
        fix_bulk_fraction = True
    else:
        fix_bulk_fraction = False        
    
    print(fix_bulk_fraction)
    
    sd = SweepDecomNano(
        input_default=config_dict["input"],
        input_config=config_dict["input_config"],
        wolfram_kernel=kernel,
        fix_bulk_fraction=fix_bulk_fraction,
    )
    sd.calc_input_range(resolution=resolution)
    sd.calc_sweep(savepath=output, save_interval=interval)


def run_decomnano(config_dict=None, output="result.csv", kernel=None):
    """Run DecomNano with config_dict."""

    config_dict = parse_array_in_config(config_dict)
    
    if config_dict["fix_bulk_fraction"]:
        fix_bulk_fraction = True
    else:
        fix_bulk_fraction = False        

    print(fix_bulk_fraction)

    dn = DecomNano(
        input=dict(config_dict["input"]),
        wolfram_kernel=kernel,
        fix_bulk_fraction=fix_bulk_fraction,
    )
    df = dn.solve_decomnano()
    df.to_csv(output)


@click.command()
@click.option(
    "-s",
    "--sweep",
    type=bool,
    default=False,
    required=False,
    help="Sweep over a range of values.",
)
@click.option(
    "-c",
    "--config",
    type=str,
    default=None,
    required=None,
    help="Path to config file.",
)
@click.option(
    "-o",
    "--output",
    type=str,
    default=None,
    required=False,
    help="Path to output file.",
)
@click.option(
    "-i",
    "--interval",
    type=int,
    default=100,
    required=False,
    help="Interval of printing results in sweep.",
)
@click.option(
    "-k",
    "--kernel",
    type=str,
    default=None,
    required=False,
    help="Path to Wolfram Engine kernel.",
)
@click.option(
    "-r",
    "--resolution",
    type=float,
    default=None,
    required=False,
    help="Resolution of sweep.",
)
def main(sweep, config, output, interval, kernel, resolution):
    """Console script for DecomNano.\n
    DecomNano is a heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis.\n
    """
    if config is None:
        raise ValueError("Please specify config file.")

    config_dict = toml.load(config)

    if output is not None:
        output_filepath = output
    elif "output" in config_dict.keys():
        output_filepath = config_dict["output"]
    else:
        output_filepath = "result.csv"
        print("No output file specified. Using default output file: result.csv")

    if kernel is not None:
        pass
    elif "kernel" in config_dict.keys():
        kernel = config_dict["kernel"]

    if resolution is not None:
        pass
    elif "resolution" in config_dict.keys():
        resolution = config_dict["resolution"]
    else:
        resolution = 0.1
        print("No resolution specified. Using default resolution: 0.1")

    if sweep or config_dict["sweep"]:
        run_sweep(
            config_dict,
            output_filepath,
            interval=interval,
            kernel=kernel,
            resolution=resolution,
        )
    else:
        run_decomnano(config_dict, output_filepath, kernel=kernel)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
