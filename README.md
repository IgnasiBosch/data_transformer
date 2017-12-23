# Data Transformer

Transform data automatically using a swagger-kind-of schema definition 

positional arguments:  
  target_schema schema that will be applied to source

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  source file to transform
  -d DIRECTORY, --directory DIRECTORY source folder to transform
  -p PREFIX, --prefix PREFIX prefix to rename new files
  -t TO, --to TO        target folder to save the output


## Target Schema example
{
  "root": {
    "root_level_1": {
      "id": "source_root_level_1>uuid",
      "slug": "source_root_level_1>slug",
      "abstract": "source_root_level_1>abstract:html_unescape",
    },
    "nested_nodes": [
      "source_nested_nodes$node"
    ]
  },
  "node": {
    "node_key": "source_node_key"
  }
}