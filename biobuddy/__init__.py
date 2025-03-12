from .version import __version__

# The actual model to inherit from
from .generic.biomechanical_model import BiomechanicalModel

# Some classes to define the BiomechanicalModel
from .generic.rigidbodies.axis import Axis
from .generic.rigidbodies.inertia_parameters import InertiaParameters
from .generic.rigidbodies.marker import Marker
from .generic.rigidbodies.contact import Contact
from .generic.muscle import Muscle
from .generic.muscle_group import MuscleGroup
from .generic.via_point import ViaPoint
from .generic.mesh import Mesh
from .generic.mesh_file import MeshFile
from .protocols import Data, GenericDynamicModel
from .rotations import Rotations
from .range_of_motion import RangeOfMotion, Ranges
from .generic.segment import Segment
from .generic.segment_coordinate_system import SegmentCoordinateSystem
from .translations import Translations

# Add also the "Real" version of classes to create models from values
from .real.biomechanical_model_real import BiomechanicalModelReal
from .real.axis_real import AxisReal
from .real.marker_real import MarkerReal
from .real.contact_real import ContactReal
from .real.muscle_real import MuscleReal, MuscleType, MuscleStateType
from .real.via_point_real import ViaPointReal
from .real.mesh_real import MeshReal
from .real.mesh_file_real import MeshFileReal
from .real.segment_real import SegmentReal
from .real.segment_coordinate_system_real import SegmentCoordinateSystemReal
from .real.inertia_parameters_real import InertiaParametersReal

# The accepted data formating
from .c3d_data import C3dData

__all__ = [
    BiomechanicalModel.__name__,
    Axis.__name__,
    InertiaParameters.__name__,
    Marker.__name__,
    Contact.__name__,
    Muscle.__name__,
    MuscleGroup.__name__,
    ViaPoint.__name__,
    Mesh.__name__,
    MeshFile.__name__,
    Data.__name__,
    GenericDynamicModel.__name__,
    Rotations.__name__,
    RangeOfMotion.__name__,
    Ranges.__name__,
    Segment.__name__,
    SegmentCoordinateSystem.__name__,
    Translations.__name__,
    BiomechanicalModelReal.__name__,
    AxisReal.__name__,
    MarkerReal.__name__,
    ContactReal.__name__,
    MuscleReal.__name__,
    MuscleType.__name__,
    MuscleStateType.__name__,
    ViaPointReal.__name__,
    MeshReal.__name__,
    MeshFileReal.__name__,
    SegmentReal.__name__,
    SegmentCoordinateSystemReal.__name__,
    InertiaParametersReal.__name__,
]
