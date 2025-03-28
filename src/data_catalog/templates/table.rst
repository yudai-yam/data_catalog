{{ table_name }}
========================================

Overview
--------

- **author**: {{ author }}
- **description**: {{ description }}
{% if comments is none or comments is undefined %}
{% elif comments is iterable and (comments is not string and comments is not mapping) %}
- **comments**:
{% for comment in comments %}
  * {{ comment }}
{% endfor %}
{% else %}
- **comments**: {{ comments }}
{% endif %}
- **regression test configuration**:
{% if regression_test_config.comparison_key is iterable and (regression_test_config.comparison_key is not string and regression_test_config.comparison_key is not mapping) %}
  * *comparison key*:
  {% for comparison_key in regression_test_config.comparison_key %}
    * ``{{ comparison_key }}``
  {% endfor %}
  {% else %}
  * *comparison key*: ``{{ regression_test_config.comparison_key }}``
{% endif %}
{% if regression_test_config.columns_to_ignore is none or regression_test_config.columns_to_ignore is undefined %}
{% elif regression_test_config.columns_to_ignore is iterable and (regression_test_config.columns_to_ignore is not string and regression_test_config.columns_to_ignore is not mapping) %}
  * *columns to ignore*:
  {% for columns_to_ignore in regression_test_config.columns_to_ignore %}
    * ``{{ columns_to_ignore }}``
  {% endfor %}
  {% else %}
  * *columns to ignore*: ``{{ regression_test_config.columns_to_ignore }}``
{% endif %}
{% if regression_test_config.where_query is none or regression_test_config.where_query is undefined %}
{% else %}
  * *where query*:
      ``{{ regression_test_config.where_query }}``
{% endif %}

Columns
-------
.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - column_name
      - data_type
      - comments
    {% for column in columns %}
    * - ``{{column.column_name}}``
      - ``{{column.data_type}}``
      - {{column.comments}}
    {% endfor %}