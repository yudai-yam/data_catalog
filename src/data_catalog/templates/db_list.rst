DB List
=======

List of available DBs for data catalog

.. toctree::
    :maxdepth: 2
    :hidden:

{% for input in inputs %}
    {{ input }}/db_index
{% endfor %}

{% for input in inputs %}
- :doc:`{{ input }}/db_index`
{% endfor %}
