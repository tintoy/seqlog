Feature flags
-------------

You can change certain behaviour of the software at runtime, even after you configure Seq. You'll have to use:

.. autofunction:: seqlog.feature_flags.enable_feature

.. autofunction:: seqlog.feature_flags.disable_feature

.. autofunction:: seqlog.feature_flags.configure_feature

.. autoclass:: seqlog.feature_flags.FeatureFlag
    :members:

An example to disable ignoring of submission errors for Seq failures would look like this:

.. code-block:: python

    from seqlog.feature_flags import disable_feature, FeatureFlag
    
    disable_feature(FeatureFlag.IGNORE_SEQ_SUBMISSION_ERRORS)

