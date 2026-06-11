try:
    from simddot._core import dot
except ModuleNotFoundError as exc:
    if exc.name != 'simddot._core':
        raise
    raise ModuleNotFoundError(
        'simddot has no compute core installed. '
        "Install a platform extra, e.g. pip install 'simddot[avx2]' "
        "(or 'simddot[generic]')"
    ) from exc

__all__ = ['dot']
