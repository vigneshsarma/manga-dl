import wrapt

import utils


def cached_index(repo_name):
    @wrapt.decorator
    def caching_fn(wrapped, instance, args, kwargs):
        index_name = utils.index_location_format % (repo_name)
        index = utils.get_index_from_store(utils.config_dir, index_name)
        if index:
            return index
        print 'Downloading index for', repo_name
        index = wrapped(*args, **kwargs)
        utils.store_index(index, utils.config_dir, index_name)
        return index
    return caching_fn
