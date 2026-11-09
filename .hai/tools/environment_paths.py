"""Fixed environment layout. Legacy paths are for diagnosis/migration only."""
CONFIG = '.hai_env/config'
STATE = CONFIG + '/state.json'
PROFILES = CONFIG + '/model_profiles.json'
INSTRUCTIONS = CONFIG + '/agent_instructions.md'
LEGACY = {new: '.hai_env/' + new.rsplit('/', 1)[1]
          for new in (STATE, PROFILES, INSTRUCTIONS)}


def legacy_entries(workspace):
    """Include dangling links: invalid legacy resources must not look absent."""
    if (workspace / '.hai_env').is_symlink():
        return list(LEGACY.values())  # Do not follow an unvalidated environment ancestor.
    return [relative for relative in LEGACY.values()
            if (workspace / relative).exists() or (workspace / relative).is_symlink()]
