import openseespy.opensees as ops
from rich import print


def remove_void_nodes():
    """
    Removes free node from the model, i.e. nodes that are not attached to any element.

    Returns
    -------
    free_node_tags: list, a list containing all free nodes.
    """
    ele_tags = ops.getEleTags()
    fixed_node_tags = ops.getFixedNodes()
    all_node_valid = []
    for etag in ele_tags:
        nodes = ops.eleNodes(etag)
        all_node_valid.extend(nodes)
    all_node_valid += fixed_node_tags
    node_tags = ops.getNodeTags()
    node_invalid = list(set(node_tags) - set(all_node_valid))
    if len(node_invalid) == 0:
        print(f"Info:: The model has no free nodes!")
    else:
        for ntag in node_invalid:
            ops.remove("node", ntag)
        print(f"Info:: Free nodes with tags {node_invalid} have been removed!")
    return node_invalid
