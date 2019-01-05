HTTP Link Header Parser
=======================

Python (>= 3.6) library for parsing RFC 8288 HTTP Link headers.

.. code-block:: python3

    from httplink import parse_link_header
    result = parse_link_header('''
       <https://example.com/foo/index.html>; rel=index;
       foo*=UTF-8'en'b%c3%a5r, </path#frag>;rel="what ever"
    ''')

    ## Target URL:
    print(result['index'].target)
    # https://example.com/foo/index.html

    ## Set of link relations:
    print(result['index'].rel)
    # {'index'}

    ## Decoded attribute value:
    print(result['index']['foo'])
    # bår

    ## Raw undecoded attributes:
    print(result['index'].attributes)
    # [('rel', 'index'), ('foo*', "UTF-8'en'b%c3%a5r")]

    ## Iterate over all links:
    for link in result.links:
        print(link.rel, link.target)
    # {'index'} https://example.com/foo/index.html
    # {'ever', 'what'} /path#frag


Multiple Link headers can be parsed at the same time if you concatenate them with ``,``.

Redundant white space and comma delimiters are ignored.

``["key"]``-access is always case-insensitive.
