var flare = {
{% for x in j["mf"] %} '{{ x }}': '{{ url_for("lids:lid-graph", lid=x) }}', {% endfor %}
}