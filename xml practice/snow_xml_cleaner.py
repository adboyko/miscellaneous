"""Chop out unwanted updates  from SNOW XML Update Set
"""
import xml.etree.ElementTree as elemtree


def get_xml_tree(source):
    """Get the XML Tree
    Args:
        source -> file: THe XML source file from SNOW
    Returns:
        An XML Tree object
    """
    tree = elemtree.parse(source)
    return tree, tree.getroot()


def put_xml_file(tree):
    """Put the resulting XML Tree that was plucked
    Args:
        tree -> XML Object: The XML Tree object
    Returns:
          None
    """
    tree.write("cleaned-updateset.xml")


def pluck_unwanted_items(tree, item_type):
    """Pluck out unwanted Update items by <type>item_type</type>
    Args:
        tree -> XML Object: The XML Object tree
        item_type -> str: The desired Item type to remove from the Tree
    Returns:
        None
    """
    del_count = 0
    print(len(tree))
    for elem in tree.findall('sys_update_xml'):
        for _ in elem.iter('type'):
            if _.text == item_type:
                tree.remove(elem)
                del_count += 1
    print(f"Total removed items: {del_count}")
    print(f"Tree size after plucking: {len(tree)}")


if __name__ == "__main__":
    # Supply the XML Source file path
    xml_tree, xml_root = get_xml_tree("../some-file-path/file.xml")
    # Specify the `<type>TYPE</type> you want removed from the Update Set
    pluck_unwanted_items(xml_root, "Item-Type-Name")
    # Finally, let's save the new file to disk
    put_xml_file(xml_tree)
