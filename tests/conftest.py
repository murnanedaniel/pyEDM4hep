import pytest
import os

@pytest.fixture(scope='session')
def sample_event_file_path():
    """Fixture to provide the path to the sample EDM4hep ROOT file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Using 'sample_event.root' as it seemed more specific from your conftest
    file_path = os.path.join(base_dir, 'data', 'sample_event.root') 
    if not os.path.exists(file_path):
        pytest.fail(f"Sample data file not found: {file_path}. Ensure 'sample_event.root' exists in tests/data/")
    return file_path

@pytest.fixture(scope="session")
def sample_detector_params():
    """
    Provides a sample dictionary of detector parameters.
    Adjust these values based on your typical use case or test requirements.
    """
    return {
        "tracking_radius": 1000.0,  # Example value in mm
        "tracking_z_max": 3000.0,   # Example value in mm
        "energy_threshold": 0.05, # Example value in GeV
        # Add any other parameters your EDM4hepEvent or other classes might use
        # from detector_params during initialization or processing.
    }

@pytest.fixture(scope="session")
def sample_event_for_tests(sample_event_file_path, sample_detector_params):
    """
    Provides a loaded EDM4hepEvent (event 0) for general testing.
    This uses the corrected sample_event_file_path.
    """
    from pyedm4hep import EDM4hepEvent
    return EDM4hepEvent(file_path=sample_event_file_path, event_index=0, detector_params=sample_detector_params)

@pytest.fixture(scope="session")
def sample_event_with_particles(sample_event_file_path, sample_detector_params):
    """
    Provides a specific event (e.g., event 0) known to have interesting particles.
    This can be the same as sample_event_for_tests if event 0 is suitable,
    or a different event index if needed.
    For this example, we'll use event 0.
    """
    from pyedm4hep import EDM4hepEvent
    # IMPORTANT: Change event_index if a different event is better for particle tests
    event_idx_for_particle_tests = 0 
    event = EDM4hepEvent(file_path=sample_event_file_path, event_index=event_idx_for_particle_tests, detector_params=sample_detector_params)
    
    # Optional: Process decay tree if your particle tests rely on ancestor/descendant info
    # that requires the processed tree with collapsed IDs, etc.
    # According to planning.md, get_ancestors/get_descendants use DecayGraphHandler,
    # which might benefit from a processed tree.
    # event.decay.process_decay_tree(energy_threshold=sample_detector_params.get('energy_threshold', 0.05))
    return event

@pytest.fixture(scope="session")
def sample_particle_id(sample_event_with_particles):
    """
    Provides the ID of a specific particle from sample_event_with_particles
    that is suitable for detailed testing.
    
    IMPORTANT: You MUST inspect your 'sample_event.root' file (event 0, or the
    event_idx_for_particle_tests you chose) and select a particle ID that
    actually exists and has the characteristics you want to test (e.g., known PDG,
    parents, daughters, hits).
    """
    # === ACTION REQUIRED: REPLACE THIS LOGIC ===
    # This is a placeholder. You need to determine a valid and useful particle ID.
    # For example, if after inspecting your chosen event, particle with ID 3 is a good candidate:
    # chosen_particle_id = 3 
    
    # For now, let's try to pick the first available particle if any.
    # This is NOT ideal for robust tests, as the first particle might not have all features.
    particles_df = sample_event_with_particles.get_particles_df()
    if not particles_df.empty:
        # Example: Pick the first particle by its DataFrame index (which should be its ID)
        # You should replace this with a hardcoded, known good ID from your data inspection.
        chosen_particle_id = particles_df.index[0] 
    else:
        pytest.fail(f"No particles found in the event (index {sample_event_with_particles.event_index}) loaded by "
                    f"'sample_event_with_particles' fixture. Cannot select a 'sample_particle_id'.")
        return None # Should not be reached

    # Sanity check: ensure the chosen particle ID can be retrieved
    try:
        particle_check = sample_event_with_particles.get_particle(chosen_particle_id)
        if particle_check is None: # Should not happen if get_particles_df() was consistent
             pytest.fail(f"Particle with ID {chosen_particle_id} could not be retrieved from the event, "
                         f"even though it was found in particles_df. Fixture setup issue.")
    except Exception as e: # Catch any error during get_particle, e.g. if ID is truly invalid
        pytest.fail(f"Error retrieving particle with ID {chosen_particle_id} for 'sample_particle_id' fixture: {e}")

    return chosen_particle_id

# You would then define other fixtures like:
# sample_event_with_particles, sample_particle_id,
# sample_event_with_hits, sample_tracker_hit_global_id, etc.
# These might load specific events or identify specific elements within
# your sample_event_for_tests or another loaded event.

# For example:
# @pytest.fixture(scope="session")
# def sample_event_with_particles(sample_event_file_path, sample_detector_params):
#     # You might choose a specific event index known to have interesting particles
#     from pyedm4hep import EDM4hepEvent
#     event = EDM4hepEvent(file_path=sample_event_file_path, event_index=1, detector_params=sample_detector_params) # e.g. event 1
#     # Optionally process decay tree if tests depend on it
#     # event.decay.process_decay_tree(energy_threshold=sample_detector_params.get('energy_threshold', 0.01))
#     return event

# @pytest.fixture(scope="session")
# def sample_particle_id(sample_event_with_particles):
#     # Logic to pick a particle ID from sample_event_with_particles
#     # This needs to be a particle that actually exists and is useful for testing
#     particles_df = sample_event_with_particles.get_particles_df()
#     if not particles_df.empty:
#         # Example: return the ID of the first particle.
#         # You should pick an ID that makes sense for your tests.
#         return particles_df.index[0]
#     pytest.fail("No particles found in sample_event_with_particles for sample_particle_id fixture.")
#     return None # Should not be reached if fail works 