# Yaml with dict key order respected - see:
# http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
# JJW

import yaml
from collections import OrderedDict
from pprint import pprint

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        #print 'NODE', node.start_mark.line, node.start_mark.column
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

# usage example:
# ordered_load(stream, yaml.SafeLoader)

lines = {}

def ordered_load_all (stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        #print 'NODE #############', node.start_mark.line, node.start_mark.column, node.value [0][0]
        #if isinstance (node.value [0][0].value, (str, unicode)):
        #  lines [node.value[0][0].value] = node.start_mark.line
          
        def add_line_map (node):
          if hasattr (node, 'value'):
            if isinstance (node.value, (str, unicode)):
              lines [node.value] = node.start_mark.line
            else:
              #print type (node.value)  # all 'list'
              for subnode in node.value:
                #print subnode [0]
                add_line_map (subnode [0])
            
        add_line_map (node)

        # nope, these don't work, as the nodes are primitive types by the time they're loaded:
        #node._line = node.start_mark.line
        #node._column = node.start_mark.column

        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load_all(stream, OrderedLoader)


#For serialization, I don't know an obvious generalization, 
# but at least this shouldn't have any side effects:

def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

# usage:
# ordered_dump(data, Dumper=yaml.SafeDumper)

