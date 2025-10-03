Table List
==========

List of tables in {{db_name}} database.

.. toctree::
    :maxdepth: 1
    :hidden:

{% for table in json_input.keys() %}
    tables/{{ table }}
{% endfor %}

{% for table, value in json_input.items() %}
- :doc:`tables/{{ table }}`
    - *author*: {{ value.author }}
    - *description*: {{ value.description }}
{% endfor %}
