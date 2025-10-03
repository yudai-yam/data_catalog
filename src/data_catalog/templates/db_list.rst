DB List
=======

List of available DBs for data catalog

.. toctree::
    :maxdepth: 1

{% for input in inputs %}
    {{ input }}/db_index
{% endfor %}

