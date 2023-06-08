import warnings

def instance_exist(instance_name_id,
                   instances_index: dict,
                   warn_user: bool,
                   warn_mode: str) -> bool:
    """Check if an instance identified by a name or a number in a class index.

    Args:
        instance_name_id (Any): instance's identifier
        instances_index (dict): class index
        warn_user (bool): send a warning to the user.
        warn_mode (str): warn either when the anime is missing or if it\
            exists : "missing" or "presence" respectively.

    Returns:
        bool: if the instance exists or not.
    """
    if instance_name_id in instances_index.keys():
        if warn_user and warn_mode == "presence":
            warnings.warn("An instance with the same id already exist, \
ignoring it.")
        return True
    else:
        if warn_user and warn_mode == "missing":
            warnings.warn("Not any instance with this id exists in \
AnimeTime database, ignoring it.")
        return False


def delete_instance(instances_index: dict, instances_list: list = None) -> None:
    """Delete instances from their identifier and the linked index.

    Args:
        instances_index (dict): index related to the instances.
        instances_list (list, optional): list of the instances to delete.
        Defaults to None.
    """
    instances_list = select_all_instances(instances_index, instances_list)
    for instance_to_delete in instances_list:
        if instance_exist(instance_to_delete,
                          instances_index,
                          True,
                          "missing"):
            del instances_index[instance_to_delete]


def select_all_instances(instances_index: dict,
                         instances_list: list = None) -> list:
    """Return all the instances of their index if instances_list == None.

    Args:
        instances_index (dict): index of the instances
        instances_list (list, optional): list of the instances.
        Defaults to None.

    Returns:
        list: instances list
    """
    if instances_list is None:
        return list(instances_index.keys())
    return instances_list