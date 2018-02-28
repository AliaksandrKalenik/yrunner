from graphviz import Digraph

from alesya.models import Location


class LocationNode(object):

    def __init__(self, location_id, name, children=None):
        self.location_id = location_id
        self.name = name
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def to_dot(self, dot):
        for child in self.children:
            dot.node(str(child.location_id), child.name)
            dot.edge(str(self.location_id), str(child.location_id), constraint='false')
            child.to_dot(dot)

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.name)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

    @staticmethod
    def tree_to_dot(tree, filename):
        dot = Digraph("ERIP", format='svg', comment='ERIP Locations')
        for child in tree.children:
            dot.node(str(child.location_id), child.name)
            dot.edge(str(tree.location_id), str(child.location_id))
            child.to_dot(dot)
        dot.render(filename+".dot")

    @staticmethod
    def get_location_tree():
        root = LocationNode(None, "ERIP")

        def make_tree(parent_node):
            parent = Location.objects.filter(id=parent_node.location_id).first()
            children = parent.children.all()
            for child in children:
                child_node = LocationNode(child.child.id, child.child.name)
                parent_node.add_child(child_node)
                make_tree(child_node)

        parents = Location.objects.filter(parents=None).distinct().all()
        for parent in parents:
            parent_node = LocationNode(parent.id, parent.name)
            make_tree(parent_node)
            root.add_child(parent_node)
        return root
