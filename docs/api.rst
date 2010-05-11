===
API
===

.. automodule:: skeleton
    :members:


.. autoclass:: skeleton.Skeleton
    :members: run, template_formatter, cmd, configure_parser, src, vars, file_encoding, required_skeletons
    
    .. automethod:: check_variables()
    .. automethod:: get_missing_variables()
    .. automethod:: write(dst_dir, run_dry=False)
    

.. autoclass:: skeleton.Var
    :members: display_name, full_description, prompt, validate
    

.. autofunction:: skeleton.insert_into_file