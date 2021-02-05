# Developers guide

## What code should I write

You can contribute directly to UCTT or you can write your own UCTT objects in any
python package/module.

If you want to write code to consume in your own testing efforts, then feel free
to write the code in your test-suites or as reusable python modules.
All that is needed to active is to import any modules which contain the mtt
decorater usage.

If you have some code that could be usable to other UCTT testers, feel free to
contribute directly to the mtt repository.

Consider the following targets:

### UCTT

core functionality for contrib and plugin managing, as well as definition of
types of plugins.
the core is written in such a way that you can throw away the rest of the code
and use it for anything, if you don't like the constraints put in place.

### dummy

Plugins that meet requirements for usage but don't actually do anything.

## Writing a plugin

@TODO

## Injecting my plugin into my code.

@TODO
