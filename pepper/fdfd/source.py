from abc import ABC, abstractmethod
from enum import Enum
from pydantic import create_model

from tidy3d import GaussianPulse
import tidy3d.components.source as tidy3d_src

from ..constants import C_0
from .source_init import dict_src_init


DUMMY_WL = 1.55 * 1e-6
DUMMY_FREQ = C_0 / DUMMY_WL
DUMMY_FACTOR = 0.1
DUMMY_SRC_CLASS = GaussianPulse


class SimulationType(Enum):
    FDTD = "fdtd"
    FDFD = "fdfd"


# TODO: Do we really need to use the freq0 for a source?
class DummySource(DUMMY_SRC_CLASS):
    def __init__(self, freq):
        super(DummySource, self).__init__(
            freq0=freq,
            fwidth=DUMMY_FACTOR * freq,
        )

# DummySource = DUMMY_SRC_CLASS(
#     freq0=DUMMY_FREQ,
#     fwidth=DUMMY_FACTOR * DUMMY_FREQ,
# )


from typing import Optional, List



# def _tidy3d_fdfd_monkey_patch(Tidy3DClass):
#     additional_fdfd_fields = {
#         'amplitude': 1.0,
#         'phase': 0.0,
#         'simulation_type': SimulationType.FDFD,
#         'wl': 0
#     }
#     return create_model(
#         Tidy3DClass.__name__,
#         # allow_mutation=True,
#         # frozen=False,
#         # allow_population_by_field_name=True,
#         __base__=Tidy3DClass,
#         source_time=DummySource,
#         source_initialization=dict_src_init,#[Tidy3DClass.__name__],
#         **additional_fdfd_fields,
#     )

def _tidy3d_fdfd_monkey_patch(Tidy3DClass):
    def fun_add_fields(sim_freq=None, sim_wl=None, **kwds):
        if sim_freq is None and sim_wl is None:
            raise ValueError("Provide either 'sim_freq' or 'sim_wl'.")
        elif sim_freq is not None and sim_wl is not None:
            raise ValueError("Provide only one field: 'sim_freq' or 'sim_wl'.")
        elif sim_freq is None:
            sim_freq = C_0 / sim_wl
        else:
            sim_wl = C_0 / sim_freq

        additional_fdfd_fields = {
            'amplitude': 1.0,
            'phase': 0.0,
            'simulation_type': SimulationType.FDFD,
        }

        model = create_model(
            Tidy3DClass.__name__,
            __base__=Tidy3DClass,
            sim_freq=sim_freq,
            sim_wl=sim_wl,
            source_time=DummySource(sim_freq),
            source_initialization=dict_src_init,#[Tidy3DClass.__name__],
            **additional_fdfd_fields,
        )
        return model(**kwds)
    return fun_add_fields

    # return create_model(
    #     Tidy3DClass.__name__,
    #     # allow_mutation=True,
    #     # frozen=False,
    #     # allow_population_by_field_name=True,
    #     __base__=Tidy3DClass,
    #     source_time=DummySource,
    #     source_initialization=dict_src_init,#[Tidy3DClass.__name__],
    #     **additional_fdfd_fields,
    # )



PlaneWaveFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.PlaneWave)
UniformCurrentSourceFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.UniformCurrentSource)
PointDipoleFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.PointDipole)
GaussianBeamFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.GaussianBeam)
# AstigmaticGaussianBeamFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.AstigmaticGaussianBeam)
AstigmaticGaussianBeamFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.GaussianBeam)
ModeSourceFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.ModeSource)
# PlaneWaveFdfd = _tidy3d_fdfd_monkey_patch(tidy3d_src.PlaneWave)


# class PlaneWaveFdfd(tidy3d_src.PlaneWave):
#     amplitude: float = 1.0,
#     phase: float = 0.0,
#     simulation_type: SimulationType = SimulationType.FDFD,
#     test_field: Optional[List[int]] = None,
#     source_time = DummySource



class SourceFdfd(ABC):
    # @abstractmethod
    def _init_source(self):
        pass



# import numpy as np

# fdfd_fields = {
#     'source_time': DummySource(DUMMY_FREQ),
#     'simulation_type': SimulationType.FDFD,
#     'amplitude': 1.0,
#     'phase': 0.0,
#     'src_inds': list[int]
# }

# def _tidy3d_fdfd_monkey_patch_class2(
#     Tidy3DClass,
#     amplitude: float = 1.0,
#     phase: float = 0.0
# ):
#     model = create_model(
#         Tidy3DClass.__name__,
#         **fdfd_fields,
#         source_initialization=dict_src_init[Tidy3DClass.__name__],
#         __base__=Tidy3DClass,
#     )
#     return model

# PlaneWaveFdfd2 = _tidy3d_fdfd_monkey_patch_class2(tidy3d_src.PlaneWave)


# # class SourceModel()

