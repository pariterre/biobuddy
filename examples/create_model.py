#
# This examples shows how to
#     1. Create a model from scratch using specified dimensions (model_creation_from_static)
#     2. Create a complex model from scratch (complex_model_from_scratch)
#     3. Create a model from scratch using a template with marker names (model_creation_from_data)
#
# Please note that this example will work only with the Eigen backend
#

import os
from pathlib import Path

import numpy as np
from biobuddy import (
    BiomechanicalModel,
    BiomechanicalModelReal,
    MarkerReal,
    MeshReal,
    MeshFile,
    Segment,
    SegmentReal,
    SegmentCoordinateSystemReal,
    Contact,
    MuscleGroup,
    Muscle,
    MuscleType,
    MuscleStateType,
    Translations,
    Rotations,
    RangeOfMotion,
    Ranges,
    ViaPoint,
)


def model_creation_from_static_trial(remove_temporary: bool = True):
    """
    We define a new model by feeding in the actual dimension and position of the model
    Please note that a bunch of useless markers are defined, this is for the other model creation below which needs them
    to define the SegmentCoordinateSystem matrices
    """

    kinematic_model_file_path = "body.bioMod"

    # Create a model holder
    bio_model = BiomechanicalModelReal()

    # The trunk segment
    bio_model.segments["TRUNK"] = SegmentReal(
        name="TRUNK",
        translations=Translations.YZ,
        rotations=Rotations.X,
        mesh=MeshReal(((0, 0, 0), (0, 0, 0.53))),
    )
    bio_model.segments["TRUNK"].add_marker(MarkerReal(name="PELVIS", parent_name="TRUNK"))

    # The head segment
    bio_model.segments["HEAD"] = SegmentReal(
        name="HEAD",
        parent_name="TRUNK",
        segment_coordinate_system=SegmentCoordinateSystemReal.from_euler_and_translation(
            (0, 0, 0), "xyz", (0, 0, 0.53)
        ),
        mesh=MeshReal(((0, 0, 0), (0, 0, 0.24))),
    )
    bio_model.segments["HEAD"].add_marker(MarkerReal(name="BOTTOM_HEAD", parent_name="HEAD", position=(0, 0, 0)))
    bio_model.segments["HEAD"].add_marker(MarkerReal(name="TOP_HEAD", parent_name="HEAD", position=(0, 0, 0.24)))
    bio_model.segments["HEAD"].add_marker(MarkerReal(name="HEAD_Z", parent_name="HEAD", position=(0, 0, 0.24)))
    bio_model.segments["HEAD"].add_marker(MarkerReal(name="HEAD_XZ", parent_name="HEAD", position=(0.24, 0, 0.24)))

    # The arm segment
    bio_model.segments["UPPER_ARM"] = SegmentReal(
        name="UPPER_ARM",
        parent_name="TRUNK",
        segment_coordinate_system=SegmentCoordinateSystemReal.from_euler_and_translation(
            (0, 0, 0), "xyz", (0, 0, 0.53)
        ),
        rotations=Rotations.X,
        mesh=MeshReal(((0, 0, 0), (0, 0, -0.28))),
    )
    bio_model.segments["UPPER_ARM"].add_marker(MarkerReal(name="SHOULDER", parent_name="UPPER_ARM", position=(0, 0, 0)))
    bio_model.segments["UPPER_ARM"].add_marker(
        MarkerReal(name="SHOULDER_X", parent_name="UPPER_ARM", position=(1, 0, 0))
    )
    bio_model.segments["UPPER_ARM"].add_marker(
        MarkerReal(name="SHOULDER_XY", parent_name="UPPER_ARM", position=(1, 1, 0))
    )

    bio_model.segments["LOWER_ARM"] = SegmentReal(
        name="LOWER_ARM",
        parent_name="UPPER_ARM",
        segment_coordinate_system=SegmentCoordinateSystemReal.from_euler_and_translation(
            (0, 0, 0), "xyz", (0, 0, -0.28)
        ),
        mesh=MeshReal(((0, 0, 0), (0, 0, -0.27))),
    )
    bio_model.segments["LOWER_ARM"].add_marker(MarkerReal(name="ELBOW", parent_name="LOWER_ARM", position=(0, 0, 0)))
    bio_model.segments["LOWER_ARM"].add_marker(MarkerReal(name="ELBOW_Y", parent_name="LOWER_ARM", position=(0, 1, 0)))
    bio_model.segments["LOWER_ARM"].add_marker(MarkerReal(name="ELBOW_XY", parent_name="LOWER_ARM", position=(1, 1, 0)))

    bio_model.segments["HAND"] = SegmentReal(
        name="HAND",
        parent_name="LOWER_ARM",
        segment_coordinate_system=SegmentCoordinateSystemReal.from_euler_and_translation(
            (0, 0, 0), "xyz", (0, 0, -0.27)
        ),
        mesh=MeshReal(((0, 0, 0), (0, 0, -0.19))),
    )
    bio_model.segments["HAND"].add_marker(MarkerReal(name="WRIST", parent_name="HAND", position=(0, 0, 0)))
    bio_model.segments["HAND"].add_marker(MarkerReal(name="FINGER", parent_name="HAND", position=(0, 0, -0.19)))
    bio_model.segments["HAND"].add_marker(MarkerReal(name="HAND_Y", parent_name="HAND", position=(0, 1, 0)))
    bio_model.segments["HAND"].add_marker(MarkerReal(name="HAND_YZ", parent_name="HAND", position=(0, 1, 1)))

    # The thigh segment
    bio_model.segments["THIGH"] = SegmentReal(
        name="THIGH",
        parent_name="TRUNK",
        rotations=Rotations.X,
        mesh=MeshReal(((0, 0, 0), (0, 0, -0.42))),
    )
    bio_model.segments["THIGH"].add_marker(MarkerReal(name="THIGH_ORIGIN", parent_name="THIGH", position=(0, 0, 0)))
    bio_model.segments["THIGH"].add_marker(MarkerReal(name="THIGH_X", parent_name="THIGH", position=(1, 0, 0)))
    bio_model.segments["THIGH"].add_marker(MarkerReal(name="THIGH_Y", parent_name="THIGH", position=(0, 1, 0)))

    # The shank segment
    bio_model.segments["SHANK"] = SegmentReal(
        name="SHANK",
        parent_name="THIGH",
        segment_coordinate_system=SegmentCoordinateSystemReal.from_euler_and_translation(
            (0, 0, 0), "xyz", (0, 0, -0.42)
        ),
        rotations=Rotations.X,
        mesh=MeshReal(((0, 0, 0), (0, 0, -0.43))),
    )
    bio_model.segments["SHANK"].add_marker(MarkerReal(name="KNEE", parent_name="SHANK", position=(0, 0, 0)))
    bio_model.segments["SHANK"].add_marker(MarkerReal(name="KNEE_Z", parent_name="SHANK", position=(0, 0, 1)))
    bio_model.segments["SHANK"].add_marker(MarkerReal(name="KNEE_XZ", parent_name="SHANK", position=(1, 0, 1)))

    # The foot segment
    bio_model.segments["FOOT"] = SegmentReal(
        name="FOOT",
        parent_name="SHANK",
        segment_coordinate_system=SegmentCoordinateSystemReal.from_euler_and_translation(
            (-np.pi / 2, 0, 0), "xyz", (0, 0, -0.43)
        ),
        rotations=Rotations.X,
        mesh=MeshReal(((0, 0, 0), (0, 0, 0.25))),
    )
    bio_model.segments["FOOT"].add_marker(MarkerReal(name="ANKLE", parent_name="FOOT", position=(0, 0, 0)))
    bio_model.segments["FOOT"].add_marker(MarkerReal(name="TOE", parent_name="FOOT", position=(0, 0, 0.25)))
    bio_model.segments["FOOT"].add_marker(MarkerReal(name="ANKLE_Z", parent_name="FOOT", position=(0, 0, 1)))
    bio_model.segments["FOOT"].add_marker(MarkerReal(name="ANKLE_YZ", parent_name="FOOT", position=(0, 1, 1)))

    # Put the model together, print it and print it to a bioMod file
    bio_model.write(kinematic_model_file_path)

    if remove_temporary:
        os.remove(kinematic_model_file_path)


def complex_model_from_scratch(mesh_path, remove_temporary: bool = True):
    """
    We define a new model by feeding in the actual dimension and position of the model.
    Please note that this model is not a human, it is only used to show the functionalities of the model creation module.
    """

    kinematic_model_file_path = "muscled_pendulum.bioMod"

    # Create a model holder
    bio_model = BiomechanicalModel()

    # The ground segment
    bio_model.segments["GROUND"] = Segment(name="GROUND")

    # The pendulum segment
    bio_model.segments["PENDULUM"] = Segment(
        name="PENDULUM",
        translations=Translations.XYZ,
        rotations=Rotations.X,
        q_ranges=RangeOfMotion(range_type=Ranges.Q, min_bound=[-1, -1, -1, -np.pi], max_bound=[1, 1, 1, np.pi]),
        qdot_ranges=RangeOfMotion(
            range_type=Ranges.Qdot, min_bound=[-10, -10, -10, -np.pi * 10], max_bound=[10, 10, 10, np.pi * 10]
        ),
        mesh_file=MeshFile(
            mesh_file_name=mesh_path,
            mesh_color=np.array([0, 0, 1]),
            scaling_function=lambda m: np.array([1, 1, 10]),
            rotation_function=lambda m: np.array([np.pi / 2, 0, 0]),
            translation_function=lambda m: np.array([0.1, 0, 0]),
        ),
    )
    # The pendulum segment contact point
    bio_model.segments["PENDULUM"].add_contact(
        Contact(
            name="PENDULUM_CONTACT",
            function=lambda m: np.array([0, 0, 0]),
            parent_name="PENDULUM",
            axis=Translations.XYZ,
        )
    )

    # The pendulum muscle group
    bio_model.muscle_groups["PENDULUM_MUSCLE_GROUP"] = MuscleGroup(
        name="PENDULUM_MUSCLE_GROUP", origin_parent_name="GROUND", insertion_parent_name="PENDULUM"
    )

    # The pendulum muscle
    bio_model.muscles["PENDULUM_MUSCLE"] = Muscle(
        "PENDULUM_MUSCLE",
        muscle_type=MuscleType.HILLTHELEN,
        state_type=MuscleStateType.DEGROOTE,
        muscle_group="PENDULUM_MUSCLE_GROUP",
        origin_position_function=lambda m: np.array([0, 0, 0]),
        insertion_position_function=lambda m: np.array([0, 0, 1]),
        optimal_length_function=lambda model, m: 0.1,
        maximal_force_function=lambda m: 100.0,
        tendon_slack_length_function=lambda model, m: 0.05,
        pennation_angle_function=lambda model, m: 0.05,
        maximal_excitation=1,
    )
    bio_model.via_points["PENDULUM_MUSCLE"] = ViaPoint(
        "PENDULUM_MUSCLE",
        position_function=lambda m: np.array([0, 0, 0.5]),
        parent_name="PENDULUM",
        muscle_name="PENDULUM_MUSCLE",
        muscle_group="PENDULUM_MUSCLE_GROUP",
    )

    # Put the model together, print it and print it to a bioMod file
    bio_model.write(kinematic_model_file_path, {})

    if remove_temporary:
        os.remove(kinematic_model_file_path)


def main():
    # Create the model from user defined dimensions
    model_creation_from_static_trial(remove_temporary=False)

    # Cre a complex model from scratch
    complex_model_from_scratch(mesh_path=f"fake.stl", remove_temporary=False)


if __name__ == "__main__":
    main()
