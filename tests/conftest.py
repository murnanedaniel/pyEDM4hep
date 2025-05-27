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

# Fixtures for test_decay.py
@pytest.fixture(scope="session")
def sample_event_for_decay_tests(sample_event_for_tests):
    """Event fixture for decay tests. For now, reuses sample_event_for_tests (event 0)."""
    # Later, you can make this load a different event index if event 0 is not ideal for decay tests.
    # from pyedm4hep import EDM4hepEvent
    # event = EDM4hepEvent(file_path=sample_event_file_path, event_index=SPECIFIC_EVENT_FOR_DECAY, detector_params=sample_detector_params)
    # event.decay.process_decay_tree() # Ensure tree is processed if tests depend on it
    # return event
    return sample_event_for_tests 

@pytest.fixture(scope="session")
def sample_particle_id_for_decay(sample_particle_id):
    """Particle ID for decay tests. For now, reuses sample_particle_id.
    IMPORTANT: Ensure this particle ID is suitable for testing decay chains in the event 
    loaded by sample_event_for_decay_tests.
    """
    # chosen_particle_id_for_decay = YOUR_ACTUAL_ID_FOR_DECAY_TESTS
    # return chosen_particle_id_for_decay
    return sample_particle_id # Placeholder: assumes the general sample_particle_id is also good for decay tests

# Fixtures for test_hits.py
@pytest.fixture(scope="session")
def sample_event_with_hits(sample_event_for_tests):
    """Event fixture for hit tests. For now, reuses sample_event_for_tests (event 0)."""
    # Later, ensure this event (e.g., event 0) has various hits for testing.
    return sample_event_for_tests

@pytest.fixture(scope="session")
def sample_tracker_hit_global_id(sample_event_with_hits):
    """Global ID of a tracker hit for testing.
    IMPORTANT: Inspect event from sample_event_with_hits and pick a VALID tracker hit ID.
    """
    # === ACTION REQUIRED: REPLACE THIS LOGIC ===
    tracker_hits_df = sample_event_with_hits.get_tracker_hits_df()
    if not tracker_hits_df.empty:
        # Example: Pick the first tracker hit. Replace with a specific, known good ID.
        return tracker_hits_df.index[0] 
    pytest.fail(f"No tracker hits found in event {sample_event_with_hits.event_index} for sample_tracker_hit_global_id fixture.")
    return None 

@pytest.fixture(scope="session")
def sample_calo_hit_global_id(sample_event_with_hits):
    """Global ID of a calorimeter hit for testing.
    IMPORTANT: Inspect event from sample_event_with_hits and pick a VALID calo hit ID.
    """
    # === ACTION REQUIRED: REPLACE THIS LOGIC ===
    calo_hits_df = sample_event_with_hits.get_calo_hits_df()
    if not calo_hits_df.empty:
        # Example: Pick the first calo hit. Replace with a specific, known good ID.
        return calo_hits_df.index[0] 
    pytest.fail(f"No calo hits found in event {sample_event_with_hits.event_index} for sample_calo_hit_global_id fixture.")
    return None

@pytest.fixture(scope="session")
def sample_calo_contribution_global_id(sample_event_with_hits):
    """Global ID of a calo contribution for testing.
    IMPORTANT: Inspect event from sample_event_with_hits and pick a VALID calo contribution ID.
    """
    # === ACTION REQUIRED: REPLACE THIS LOGIC ===
    contrib_df = sample_event_with_hits.get_calo_contributions_df()
    if not contrib_df.empty:
        # Example: Pick the first contribution. Replace with a specific, known good ID.
        return contrib_df.index[0]
    pytest.fail(f"No calo contributions found in event {sample_event_with_hits.event_index} for sample_calo_contribution_global_id fixture.")
    return None

# Fixtures for test_plotting.py
@pytest.fixture(scope="session")
def sample_event_for_plotting(sample_event_for_tests):
    """Event fixture for plotting tests. For now, reuses sample_event_for_tests (event 0)."""
    # Ensure this event has detector_params and is suitable for various plots.
    # from pyedm4hep import EDM4hepEvent
    # event = EDM4hepEvent(file_path=sample_event_file_path, event_index=SPECIFIC_EVENT_FOR_PLOTTING, detector_params=sample_detector_params)
    # event.decay.process_decay_tree() # Optional
    # return event
    return sample_event_for_tests

@pytest.fixture(scope="session")
def sample_particle_id_for_plotting(sample_particle_id):
    """Particle ID for plotting tests. For now, reuses sample_particle_id.
    IMPORTANT: Ensure this particle is suitable for plotting within the event 
    loaded by sample_event_for_plotting.
    """
    # chosen_particle_id_for_plotting = YOUR_ACTUAL_ID_FOR_PLOTTING_TESTS
    # return chosen_particle_id_for_plotting
    return sample_particle_id # Placeholder

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